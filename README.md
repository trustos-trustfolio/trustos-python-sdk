# Trust OS Python SDK

Official Python SDK for the Trust OS Decision Verification API.

---

## What is Trust OS?

Trust OS is a Decision Verification Platform that helps organizations verify high-impact decisions before execution.

- Decision verification
- Risk evaluation
- Policy enforcement
- Auditability
- Explainability
- API-first integration

---

## Features

- Pythonic client
- requests-based
- Typed exceptions
- Easy integration

---

## Quick Start

```bash
pip install git+https://github.com/trustos-trustfolio/trustos-python-sdk.git
```

Once published to PyPI:

```bash
pip install trustos
```

```python
from trustos import TrustOSClient

client = TrustOSClient(api_key="YOUR_API_KEY")

result = client.verify_decision({
    "action": "stablecoin_transfer",
    "amount": 50000,
    "currency": "USDC",
    "destination": "wallet_abc",
})

print(result["recommendation"])  # APPROVE | REVIEW | DENY
print(result["proof_hash"])       # SHA-256: 0x4a3f...9c2b
```

Use an environment variable instead of hardcoding:

```bash
# .env (never commit this file)
TRUSTOS_API_KEY=your_api_key_here
```

```python
from trustos import TrustOSClient

client = TrustOSClient()  # reads TRUSTOS_API_KEY from environment
```

---

## Examples

### Stablecoin Payment

```python
from trustos import TrustOSClient

client = TrustOSClient()

result = client.verify_decision({
    "action": "stablecoin_transfer",
    "amount": 250000,
    "currency": "USDC",
    "destination": "wallet_0x4f3b9c2a8d1e6f5a",
    "source": "Payment API",
    "priority": "High",
    "metadata": {"region": "SG", "workflow": "merchant_settlement"},
})

if result["recommendation"] == "APPROVE":
    print("Approved:", result["decision_id"])
elif result["recommendation"] == "REVIEW":
    queue_for_review(result["decision_id"])
else:
    raise ValueError("Payment denied by Trust OS policy")
```

### Treasury Disbursement

```python
result = client.verify_decision({
    "action": "treasury_disbursement",
    "amount": 1_000_000,
    "currency": "USDC",
    "destination": "dao_multisig_0x91a3b7c2",
    "source": "governance-system",
    "priority": "High",
})
```

### AI Agent Action

```python
result = client.verify_decision({
    "action": "execute_tool",
    "destination": "write_operation",
    "source": "agent-framework",
    "priority": "High",
    "metadata": {"tool": "write_record", "agent_id": "agent_alpha_001"},
})
```

More examples in the [`examples/`](./examples/) directory.

---

## API Reference

### `TrustOSClient(api_key=None, base_url=None, timeout=10.0)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str \| None` | `None` | API key. Falls back to `TRUSTOS_API_KEY` env var. |
| `base_url` | `str \| None` | Production gateway | Override the API base URL. |
| `timeout` | `float` | `10.0` | Request timeout in seconds. |

### `client.verify_decision(payload: dict) -> dict`

| Field | Type | Required | Description |
|---|---|---|---|
| `action` | string | **Yes** | Decision action type |
| `amount` | number | No | Transaction amount |
| `currency` | string | No | Currency or asset symbol |
| `destination` | string | No | Target wallet or account |
| `source` | string | No | Originating system |
| `priority` | string | No | `"High"`, `"Medium"`, or `"Low"` |
| `metadata` | object | No | Additional context fields |

**Response fields:** `decision_id`, `recommendation`, `risk_score`, `risk_level`, `policy`, `proof_hash`, `verified`, `latency_ms`

### `client.verify(payload: dict) -> dict`

Alias for `verify_decision()`.

---

## Error Handling

```python
from trustos import TrustOSClient, TrustOSError

client = TrustOSClient()

try:
    result = client.verify_decision({"action": "stablecoin_transfer"})
except TrustOSError as e:
    print(f"Status code:   {e.status_code}")
    print(f"Response body: {e.response_body}")
    print(f"Message:       {e}")
```

`TrustOSError` is raised on non-2xx responses, network errors, and invalid JSON.

---

## Documentation

- Website: https://trust-os.io
- Developer Docs: https://trust-os.io/docs
- OpenAPI: https://trust-os.io/openapi.json

---

## License

MIT
