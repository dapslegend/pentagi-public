"""Public feature flags. Aggressive paths stay off."""

FLAGS = {
    "web3_audit": True,
    "web2_hunt": False,
    "aggressive_scan": False,
    "broadcast_tx": False,
    "docker_exec": False,
    "live_llm": False,
}


def enabled(name: str) -> bool:
    return bool(FLAGS.get(name, False))
