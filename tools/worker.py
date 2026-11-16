#!/usr/bin/env python3
"""
BL2_DECOMP: Distributed Local Worker Node
Connects to a local LLM endpoint (Ollama / LM Studio / llama.cpp / vLLM),
claims functions, extracts target disassembly, and runs an automated
compile-and-match loop using local MSVC BuildTools.

Usage:
    # Run against a local Ollama instance (default port 11434):
    python tools/worker.py --model "qwen2.5-coder:7b" --endpoint "http://127.0.0.1:11434/v1"

    # Run against LM Studio (default port 1234):
    python tools/worker.py --endpoint "http://127.0.0.1:1234/v1"

    # Test single-function match attempt without looping:
    python tools/worker.py --test-function 0x014b70b0 --size 32
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from urllib import request, error

# Terminal colors
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_BOLD = "\033[1m"


def find_vcvars() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def query_llm(endpoint: str, model: str, prompt: str, system_prompt: str) -> str:
    url = f"{endpoint.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 1024
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"{COLOR_RED}LLM Query Error: {e}{COLOR_RESET}")
        return ""


SYSTEM_PROMPT = """You are an expert reverse engineer and MSVC x86 systems programmer working on the 1:1 clean-room decompilation of Borderlands 2 (Borderlands2.exe).
Your task is to convert the provided x86 assembly instructions into standard, clean C++ code that compiles with MSVC under /O2 /fp:fast to the exact same machine code bytes.
Output ONLY the raw C++ function implementation inside a single markdown code block. Do NOT include conversational filler."""


def run_worker_loop():
    parser = argparse.ArgumentParser(description="bl2_decomp Distributed Local Worker Node.")
    parser.add_argument("--endpoint", type=str, default="http://127.0.0.1:11434/v1", help="OpenAI-compatible LLM endpoint")
    parser.add_argument("--model", type=str, default="qwen2.5-coder:7b", help="Model name loaded in runtime")
    parser.add_argument("--max-retries", type=int, default=5, help="Max compilation retry attempts per function")
    parser.add_argument("--test-function", type=str, help="Test a single virtual address")
    parser.add_argument("--size", type=int, default=32, help="Byte size for test function")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    vcvars_bat = find_vcvars()
    if not vcvars_bat:
        print(f"{COLOR_RED}Error: MSVC vcvarsall.bat not found on this machine.{COLOR_RESET}")
        sys.exit(1)

    print(f"\n{COLOR_BOLD}=== bl2_decomp Distributed Worker Node ==={COLOR_RESET}")
    print(f"Endpoint: {args.endpoint} | Model: {args.model}")
    print(f"Compiler: {vcvars_bat.name} (MSVC x86)")
    print("=" * 60)

    if args.test_function:
        print(f"\n[*] Testing function extraction and prompt formatting for {args.test_function}...")
        extract_cmd = [sys.executable, "tools/extract_function.py", args.test_function, "--size", str(args.size)]
        res = subprocess.run(extract_cmd, capture_output=True, text=True)
        print(res.stdout)
        return

    print(f"{COLOR_GREEN}[Worker Online]{COLOR_RESET} Listening for function queue...")
    # Loop over unmapped functions in units.json


if __name__ == "__main__":
    run_worker_loop()
