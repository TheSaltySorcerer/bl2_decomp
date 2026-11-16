#!/usr/bin/env python3
"""
BL2_DECOMP Supervisor CLI & Review Engine
Used by Antigravity to review escalated failure clusters, inject hints/rules,
and submit verified 100% byte-matching clean-room C++ implementations.
"""

import sys
import json
import argparse
import urllib.request
from pathlib import Path

SERVER_DEFAULT = "http://localhost:8080"

def get_escalations(server_url: str):
    url = f"{server_url}/escalations"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        print(f"Error connecting to master server: {e}")
        return None

def set_hint(server_url: str, address: str, hint: str):
    url = f"{server_url}/resolve_escalation"
    payload = {
        "address": address,
        "action": "set_hint",
        "hints": hint
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error setting hint: {e}")
        return None

def set_unit_rule(server_url: str, unit: str, rule: str):
    url = f"{server_url}/resolve_escalation"
    payload = {
        "unit": unit,
        "action": "set_unit_rule",
        "hints": rule,
        "apply_to_unit": True
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error setting unit rule: {e}")
        return None

def submit_solution(server_url: str, unit: str, address: str, size: int, code: str):
    url = f"{server_url}/submit"
    payload = {
        "unit": unit,
        "address": address,
        "size": size,
        "code": code,
        "worker_id": "antigravity_supervisor"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error submitting solution: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="bl2_decomp Supervisor Controller")
    parser.add_argument("--server", type=str, default=SERVER_DEFAULT)
    subparsers = parser.add_subparsers(dest="cmd")

    list_p = subparsers.add_parser("list", help="List all escalated functions")

    hint_p = subparsers.add_parser("hint", help="Inject architectural guideline / hint for a function")
    hint_p.add_argument("address", type=str)
    hint_p.add_argument("hint_text", type=str)

    unit_p = subparsers.add_parser("unit-rule", help="Apply pattern rule to all functions across an entire unit")
    unit_p.add_argument("unit", type=str)
    unit_p.add_argument("rule_text", type=str)

    submit_p = subparsers.add_parser("submit", help="Submit verified supervisor C++ candidate")
    submit_p.add_argument("unit", type=str)
    submit_p.add_argument("address", type=str)
    submit_p.add_argument("size", type=int)
    submit_p.add_argument("code_file", type=str)

    args = parser.parse_args()

    if args.cmd == "list" or not args.cmd:
        data = get_escalations(args.server)
        if not data:
            return
        esc = data.get("escalations", {})
        print(f"\n=== bl2_decomp Escalation Queue ({len(esc)} flagged functions) ===")
        print(f"Threshold: >= {data.get('threshold', 5)} worker failures\n")
        if not esc:
            print("No functions currently escalated. Workers are progressing normally.")
            return

        for addr, item in esc.items():
            print(f"[{addr}] Unit: {item.get('unit')} | Size: {item.get('size')}B | Failures: {item.get('failure_count')}")
            print(f"  Attempted by: {', '.join(item.get('workers_attempted', []))}")
            print("  Recent Errors:")
            for err in item.get("recent_errors", []):
                print(f"    - {err[:100]}...")
            print("-" * 60)

    elif args.cmd == "hint":
        res = set_hint(args.server, args.address, args.hint_text)
        print(f"Result: {res}")

    elif args.cmd == "unit-rule":
        res = set_unit_rule(args.server, args.unit, args.rule_text)
        print(f"Result: {res}")

    elif args.cmd == "submit":
        code_path = Path(args.code_file)
        if not code_path.exists():
            print(f"File not found: {code_path}")
            return
        code = code_path.read_text(encoding="utf-8")
        res = submit_solution(args.server, args.unit, args.address, args.size, code)
        print(f"Submission Result: {res}")

if __name__ == "__main__":
    main()
