"""Stub planner. No network. No API keys."""

from __future__ import annotations


def plan(flow: dict) -> list[dict]:
    track = flow.get("track", "web3")
    if track != "web3":
        return [{"step": "refuse", "reason": "public build is web3-only"}]
    address = flow.get("target", {}).get("address", "")
    return [
        {"step": "measure_code", "tool": "web3.get_code", "address": address},
        {"step": "measure_storage", "tool": "web3.get_storage", "address": address, "slot": "0x0"},
        {"step": "checklist", "tool": "web3.checklist"},
    ]
