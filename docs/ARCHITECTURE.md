# Architecture

```
User
  └─ scripts/run_flow.py
       └─ flows.runner
            ├─ config.flags
            ├─ providers.stub_plan
            ├─ tools.registry
            │    └─ web3.read (getCode, getStorageAt, chainId)
            └─ report.json
```

A flow YAML names the track, the target address, and which tools are allowed. The runner refuses tools that are flagged off.
