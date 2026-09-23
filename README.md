# Cloud Architecture Evaluator

## Run
- Synchronize dependencies with uv
```bash
uv sync
```

## Usage
- Run audit_servive_tier method
```bash
uv run python3 src/lesson75/cloud_architecture_evaluator.py audit [workload_type: str ] [custom_os_needed]
```

- Run calulate_multiregion_budget method
```bash
uv run python3 src/lesson75/cloud_architecture_evaluator.py calculate [primary_cost: float] [replication_rate: float]
```

- Run simulate_health_check method
```bash
uv run python3 src/lesson75/cloud_architecture_evaluator.py simulate [probe_response: int ...]
```

## Stack
- uv

## Reference
[Python docs: subprocess](https://docs.python.org/3/library/argparse.html#subcommands)
[GeeksforGeeks: parseargs](https://www.geeksforgeeks.org/python/how-to-pass-a-list-as-a-command-line-argument-with-argparse/)