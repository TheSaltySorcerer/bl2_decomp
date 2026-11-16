#!/usr/bin/env python3
"""
BL2_DECOMP: Remote Cluster Worker Node
Designed to run on satellite nodes (e.g. Legion laptop, Kara's rig, ThinkPad).
Pulls tasks from kharmadesk master server, prompts local GPU (Ollama / LM Studio),
and submits candidate C++ to the master for MSVC byte-parity verification.

Usage:
    python tools/remote_worker.py --server "http://100.103.169.13:8080" --model "qwen2.5-coder:7b"
"""

import os
import sys
import time
import json
import argparse
from urllib import request, error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_BOLD = "\033[1m"


SYSTEM_PROMPT = """You are an expert reverse engineer and MSVC x86 systems programmer working on the 1:1 clean-room decompilation of Borderlands 2 (Borderlands2.exe).
Your task is to convert the provided x86 assembly instructions into standard, clean C++ code that compiles with MSVC under /O2 /fp:fast to the exact same machine code bytes.
Output ONLY the raw C++ function implementation inside a single markdown code block (```cpp ... ```). Do NOT include conversational filler."""


def query_local_llm(endpoint: str, model: str, prompt: str) -> str:
    url = f"{endpoint.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 1024
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"{COLOR_RED}Local LLM Error: {e}{COLOR_RESET}")
        return ""


def clean_code_block(raw_text: str) -> str:
    if "```cpp" in raw_text:
        return raw_text.split("```cpp")[1].split("```")[0].strip()
    elif "```" in raw_text:
        return raw_text.split("```")[1].split("```")[0].strip()
    return raw_text.strip()


def run_worker():
    parser = argparse.ArgumentParser(description="Remote Worker Node for bl2_decomp cluster.")
    parser.add_argument("--server", type=str, default="http://100.103.169.13:8080", help="Master server URL")
    parser.add_argument("--llm", type=str, default="http://127.0.0.1:11434/v1", help="Local LLM endpoint")
    parser.add_argument("--model", type=str, default="qwen2.5-coder:7b", help="Model name in local runtime")
    parser.add_argument("--worker-id", type=str, default="legion_rtx5060", help="Worker node identifier")
    args = parser.parse_args()

    print(f"\n{COLOR_BOLD}=== bl2_decomp Remote Worker Node ({args.worker_id}) ==={COLOR_RESET}")
    print(f"Master Server: {args.server}")
    print(f"Local LLM:     {args.llm} ({args.model})")
    print("=" * 66)

    while True:
        try:
            req = request.Request(f"{args.server}/task?worker_id={args.worker_id}")
            with request.urlopen(req, timeout=10) as resp:
                task = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"{COLOR_YELLOW}[Warning] Master server unreachable: {e}. Retrying in 10s...{COLOR_RESET}")
            time.sleep(10)
            continue

        if task.get("status") != "assigned":
            print(f"{COLOR_CYAN}[Idle] No tasks available. Sleeping 10s...{COLOR_RESET}")
            time.sleep(10)
            continue

        addr = task.get("address")
        fn_name = task.get("name")
        size = task.get("size")
        sig = task.get("signature")
        unit = task.get("unit")
        disasm_list = task.get("disassembly", [])

        print(f"\n{COLOR_BOLD}[Task Received]{COLOR_RESET} {addr} ({fn_name}) | {size} bytes | Unit: {unit}")

        disasm_text = "\n".join([f"  {i['address']}:  {i['bytes']:12s}  {i['mnemonic']:8s} {i['op_str']}" for i in disasm_list])

        prompt = (
            f"Target Function: {fn_name}\n"
            f"Virtual Address: {addr}\n"
            f"Size: {size} bytes\n"
            f"Signature: {sig}\n\n"
            f"x86 Disassembly from Borderlands2.exe:\n"
            f"{disasm_text}\n\n"
            f"Please generate the C++ function implementation matching this assembly."
        )

        for attempt in range(1, 4):
            print(f"  -> Generating candidate C++ (Attempt {attempt}/3)...")
            raw_response = query_local_llm(args.llm, args.model, prompt)
            candidate_code = clean_code_block(raw_response)

            if not candidate_code:
                print(f"  {COLOR_RED}[Error] Empty response from local LLM.{COLOR_RESET}")
                time.sleep(2)
                continue

            submit_payload = {
                "unit": unit,
                "address": addr,
                "size": size,
                "code": candidate_code,
                "worker_id": args.worker_id
            }

            sub_data = json.dumps(submit_payload).encode("utf-8")
            sub_req = request.Request(f"{args.server}/submit", data=sub_data, headers={"Content-Type": "application/json"})

            try:
                with request.urlopen(sub_req, timeout=15) as s_resp:
                    result = json.loads(s_resp.read().decode("utf-8"))
            except Exception as e:
                print(f"  {COLOR_RED}[Error] Failed to submit to master: {e}{COLOR_RESET}")
                break

            if result.get("status") == "accepted":
                print(f"  {COLOR_GREEN}[SUCCESS] Function {addr} matched 100% and accepted by master!{COLOR_RESET}")
                break
            else:
                err = result.get("error", "Opcode mismatch")
                print(f"  {COLOR_YELLOW}[Retry] Submission rejected: {err[:80]}...{COLOR_RESET}")
                prompt += f"\n\nPrevious candidate failed with:\n{err}\nPlease correct and retry."
                time.sleep(2)

        time.sleep(2)


if __name__ == "__main__":
    run_worker()
