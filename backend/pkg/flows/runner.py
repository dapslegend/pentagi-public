from __future__ import annotations

import json
from pathlib import Path


from backend.pkg.config import enabled
from backend.pkg.providers import plan
from backend.pkg.tools import run_tool


def load_flow(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if path.endswith((".yaml", ".yml")):
        return _mini_yaml(text)
    return json.loads(text)


def _mini_yaml(text: str) -> dict:
    """Tiny subset: key: value and one-level nested maps. Good enough for examples."""
    root: dict = {}
    stack = [root]
    indents = [-1]
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        key, _, val = raw.lstrip().partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        while indent <= indents[-1] and len(stack) > 1:
            stack.pop()
            indents.pop()
        if val == "":
            nxt: dict = {}
            stack[-1][key] = nxt
            stack.append(nxt)
            indents.append(indent)
        else:
            if val in ("true", "false"):
                stack[-1][key] = val == "true"
            else:
                stack[-1][key] = val
    return root


def run_flow(path: str | Path, rpc: str = "") -> dict:
    flow = load_flow(path)
    if flow.get("track") == "web2" or not enabled("web3_audit"):
        return {
            "status": "refused",
            "reason": "web2 and aggressive hunts are disabled in the public build",
            "flags": {
                "web2_hunt": enabled("web2_hunt"),
                "aggressive_scan": enabled("aggressive_scan"),
                "web3_audit": enabled("web3_audit"),
            },
        }
    steps = plan(flow)
    results = []
    for step in steps:
        tool = step.get("tool")
        if not tool:
            results.append(step)
            continue
        args = {k: v for k, v in step.items() if k not in ("step", "tool")}
        results.append({"step": step.get("step"), "tool": tool, "result": run_tool(tool, args, rpc=rpc)})
    return {
        "status": "completed",
        "flow": flow.get("name", str(path)),
        "track": flow.get("track"),
        "provider": "stub",
        "steps": results,
    }
