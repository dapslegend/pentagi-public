"""Read-only chain calls. Loopback RPC or fixture."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "flows" / "examples" / "fixture_code.json"
ZERO = "0x" + "00" * 32


def _code_bytes(code: str) -> int:
    if not isinstance(code, str) or code in ("0x", "0x0"):
        return 0
    return max((len(code) - 2) // 2, 0)


def _rpc(url: str, method: str, params: list) -> dict:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode())


def get_code(address: str, rpc: str = "") -> dict:
    if not rpc:
        doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
        code = doc.get("result") or "0x"
        return {
            "source": "fixture",
            "address": address or doc.get("address"),
            "code_present": _code_bytes(code) > 0,
            "bytecode_bytes": _code_bytes(code),
            "chain_id": doc.get("chain_id"),
        }
    if not rpc.startswith(("http://127.0.0.1", "http://localhost", "https://127.0.0.1")):
        return {"error": "rpc_refused", "detail": "loopback only"}
    try:
        code = (_rpc(rpc, "eth_getCode", [address, "latest"]).get("result") or "0x")
        chain = _rpc(rpc, "eth_chainId", []).get("result")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"error": "rpc_unreachable", "detail": type(exc).__name__}
    return {
        "source": "rpc",
        "address": address,
        "code_present": _code_bytes(code) > 0,
        "bytecode_bytes": _code_bytes(code),
        "chain_id": chain,
    }


def get_storage(address: str, slot: str = "0x0", rpc: str = "") -> dict:
    if not rpc:
        return {"source": "fixture", "address": address, "slot": slot, "is_zero": True}
    if not rpc.startswith(("http://127.0.0.1", "http://localhost", "https://127.0.0.1")):
        return {"error": "rpc_refused", "detail": "loopback only"}
    try:
        val = _rpc(rpc, "eth_getStorageAt", [address, slot, "latest"]).get("result") or ZERO
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"error": "rpc_unreachable", "detail": type(exc).__name__}
    return {
        "source": "rpc",
        "address": address,
        "slot": slot,
        "is_zero": val in (ZERO, "0x", "0x0"),
        "value": val,
    }
