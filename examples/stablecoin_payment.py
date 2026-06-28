"""Stablecoin payment verification example.

Verifies a cross-border USDC settlement before execution.
Gate the transfer on the APPROVE recommendation.
"""

from trustos import TrustOSClient, TrustOSError

client = TrustOSClient()

try:
    result = client.verify_decision({
        "action": "stablecoin_transfer",
        "amount": 250000,
        "currency": "USDC",
        "destination": "wallet_0x4f3b9c2a8d1e6f5a",
        "source": "Payment API",
        "priority": "High",
        "metadata": {
            "region": "SG",
            "workflow": "merchant_settlement",
        },
    })

    if result["recommendation"] == "APPROVE":
        print("✅ Payment approved — safe to execute.")
        print("   Decision ID:", result["decision_id"])
        print("   Proof Hash: ", result["proof_hash"])
    elif result["recommendation"] == "REVIEW":
        print("⏳ Payment requires human review.")
        print("   Queue decision_id for compliance team:", result["decision_id"])
    else:
        print("❌ Payment denied.")
        print("   Risk Level:", result["risk_level"])

except TrustOSError as e:
    print(f"Verification error [{e.status_code}]: {e}")
