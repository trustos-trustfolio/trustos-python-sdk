"""Basic usage example — reads API key from TRUSTOS_API_KEY env var."""

from trustos import TrustOSClient, TrustOSError

client = TrustOSClient()

try:
    result = client.verify_decision({
        "action": "stablecoin_transfer",
        "amount": 50000,
        "currency": "USDC",
        "destination": "wallet_abc",
        "source": "Payment API",
        "priority": "High",
    })
    print("Decision ID:     ", result["decision_id"])
    print("Recommendation:  ", result["recommendation"])
    print("Risk Level:      ", result["risk_level"])
    print("Risk Score:      ", result["risk_score"])
    print("Proof Hash:      ", result["proof_hash"])
    print("Latency (ms):    ", result["latency_ms"])
except TrustOSError as e:
    print(f"Verification failed [{e.status_code}]: {e}")
