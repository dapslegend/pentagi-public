from __future__ import annotations

from backend.pkg.config import enabled
from backend.pkg.web3 import checklist, read


def run_tool(name: str, args: dict, rpc: str = "") -> dict:
    if name.startswith("web2.") or name.startswith("hunt."):
        return {"error": "disabled", "tool": name, "flag": "web2_hunt"}
    if name in ("web3.broadcast", "web3.send_tx"):
        return {"error": "disabled", "tool": name, "flag": "broadcast_tx"}
    if not enabled("web3_audit") and name.startswith("web3."):
        return {"error": "disabled", "tool": name, "flag": "web3_audit"}

    if name == "web3.get_code":
        return read.get_code(args.get("address", ""), rpc=rpc)
    if name == "web3.get_storage":
        return read.get_storage(args.get("address", ""), args.get("slot", "0x0"), rpc=rpc)
    if name == "web3.checklist":
        return checklist.run()
    return {"error": "unknown_tool", "tool": name}
