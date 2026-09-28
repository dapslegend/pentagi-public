# PentAGI Public

Public cut of **PentAGI** — AI-assisted security testing platform.

This build is **web3-first**. Web2 aggressive hunts are disabled. No exploit runners. No live broadcasts. No private keys in the tree.

Author: Ayodapo Adesiyan (`dapslegend`)

## What this is

PentAGI runs **flows**: scoped review jobs with a provider, tools, and a report. The private product has multi-agent research, Docker sandboxes, and continuous hunts. This public cut keeps the flow model and the web3 audit path so people can see how a review is structured.

```
flow create → provider plan → web3 tools (read-only) → report
```

## Quick start

```bash
python3 scripts/run_flow.py --flow flows/examples/web3_audit.yaml
python3 scripts/run_flow.py --flow flows/examples/web3_audit.yaml --rpc http://127.0.0.1:8545
```

No external packages. Python 3.11+.

## Layout

```
backend/pkg/
  config/     flow defaults, feature flags
  flows/      flow runner
  providers/  stub planner (no live LLM keys required)
  tools/      tool registry
  web3/       eth_getCode / eth_getStorageAt (loopback RPC only)
frontend/src/ placeholder UI notes
flows/examples/
  web3_audit.yaml
docs/
  ARCHITECTURE.md
  SAFETY.md
scripts/
  run_flow.py
```

## Feature flags

| Flag | Public default |
|---|---|
| `web3_audit` | **on** |
| `web2_hunt` | **off** |
| `aggressive_scan` | **off** |
| `broadcast_tx` | **off** |
| `docker_exec` | **off** |
| `live_llm` | **off** (stub planner) |

See `backend/pkg/config/flags.py`.

## Safety

- RPC must be loopback (`127.0.0.1` / `localhost`) or the flow uses the offline fixture.
- Tools only call `eth_getCode`, `eth_chainId`, `eth_getStorageAt`.
- No transaction signing. No mempool watch. No web2 HTTP fuzz.
- Private operator stack, hunt dumps, and `.env` secrets are not in this repo.

## Relation to full PentAGI

Full PentAGI (private / upstream) adds GraphQL API, multi-agent orchestration, Docker tool execution, vector memory, and continuous WEB2/WEB3 hunts. This public tree is the same product shape with those aggressive paths compiled out so it is safe to clone and demo.
