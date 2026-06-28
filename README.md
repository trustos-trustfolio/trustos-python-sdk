# Trust OS Python SDK

Python SDK for the [Trust OS Decision Verification API](https://trust-os.io/docs/api).

Verify high-impact decisions before execution — payments, treasury operations, AI agent actions, and compliance workflows — with a single function call.

## Links

| Resource | URL |
|---|---|
| Website | https://trust-os.io |
| Developer Docs | https://trust-os.io/docs |
| API Reference | https://trust-os.io/docs/api |
| Playground | https://demo.trust-os.io |
| Operations Demo | https://ops.trust-os.io |
| GitHub Organization | https://github.com/trustos-trustfolio |
| OpenAPI Spec | https://trust-os.io/openapi.json |

---

## Installation

> **PyPI release coming soon.** For now, install directly from GitHub once the repository is published:

```bash
pip install git+https://github.com/trustos-trustfolio/trustos-python-sdk.git
```

Once published to PyPI:

```bash
pip install trustos
```

---

## Quick Start

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

---

## Environment Variables

Store your API key as an environment variable instead of hardcoding it:

```bash
# .env (never commit this file)
TRUSTOS_API_KEY=your_api_key_here
```

The client reads `TRUSTOS_API_KEY` automatically when no `api_key=` argument is provided:

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
    # safe to execute the transfer
    print("Approved:", result["decision_id"])
elif result["recommendation"] == "REVIEW":
    # queue for human review
    queue_for_review(result["decision_id"])
else:
    # block the transfer
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
    "destination": "database_write",
    "source": "agent-framework",
    "priority": "High",
    "metadata": {"tool": "write_record", "agent_id": "agent_alpha_001"},
})
```

More complete examples are in the [`examples/`](./examples/) directory.

---

## API Reference

### `TrustOSClient(api_key=None, base_url=None, timeout=10.0)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str \| None` | `None` | API key. Falls back to `TRUSTOS_API_KEY` env var. |
| `base_url` | `str \| None` | Production gateway | Override the API base URL. |
| `timeout` | `float` | `10.0` | Request timeout in seconds. |

Raises `ValueError` if no API key is found.

### `client.verify_decision(payload: dict) -> dict`

Submit a decision for verification. Returns the parsed JSON response.

**Request fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `action` | string | **Yes** | Decision action type |
| `amount` | number | No | Transaction amount |
| `currency` | string | No | Currency or asset symbol |
| `destination` | string | No | Target wallet or account |
| `source` | string | No | Originating system |
| `priority` | string | No | `"High"`, `"Medium"`, or `"Low"` |
| `metadata` | object | No | Additional context fields |

**Response fields:**

| Field | Type | Description |
|---|---|---|
| `decision_id` | string | Unique identifier — store for audit trail |
| `recommendation` | string | `APPROVE`, `REVIEW`, or `DENY` |
| `risk_score` | number | 0.0 (no risk) to 1.0 (maximum) |
| `risk_level` | string | `LOW`, `MEDIUM`, or `HIGH` |
| `policy` | string | Policy name and version applied |
| `proof_hash` | string | SHA-256 cryptographic proof |
| `verified` | boolean | True when cryptographically verified |
| `latency_ms` | number | Evaluation latency in milliseconds |

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

`TrustOSError` is raised on:

- Non-2xx HTTP responses (401 unauthorized, 429 rate limit, 500 server error, etc.)
- Network errors or timeouts
- Invalid JSON in the response body

---

## Security

- **Never commit your API key.** Use environment variables or a secrets manager.
- **Never hardcode keys in example scripts.** All examples use `TrustOSClient()` with no inline key.
- See [SECURITY.md](./SECURITY.md) for the vulnerability disclosure policy.

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

## License

MIT — see [LICENSE](./LICENSE).
