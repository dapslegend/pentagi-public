#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.pkg.flows import run_flow


def main() -> int:
    p = argparse.ArgumentParser(description="PentAGI public flow runner")
    p.add_argument("--flow", required=True, help="Path to flow YAML")
    p.add_argument("--rpc", default="", help="Loopback JSON-RPC only")
    args = p.parse_args()
    report = run_flow(args.flow, rpc=args.rpc)
    print(json.dumps(report, indent=2))
    if report.get("status") == "refused":
        return 2
    # fail if any tool hit rpc errors
    for step in report.get("steps") or []:
        res = step.get("result") or {}
        if res.get("error") in ("rpc_unreachable", "rpc_refused"):
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
