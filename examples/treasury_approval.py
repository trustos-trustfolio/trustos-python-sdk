"""Treasury disbursement approval example.

Verifies a DAO treasury fund release before executing on-chain.
APPROVE — proceed. REVIEW — escalate to multisig. DENY — block.
"""

from trustos import TrustOSClient, TrustOSError

client = TrustOSClient()

try:
    result = client.verify_decision({
        "action": "treasury_disbursement",
        "amount": 1_000_000,
        "currency": "USDC",
        "destination": "dao_multisig_0x91a3b7c2",
        "source": "governance-system",
        "priority": "High",
        "metadata": {
            "proposal_id": "prop_042",
            "approvals": 7,
            "quorum": 9,
        },
    })

    recommendation = result["recommendation"]
    print(f"Treasury Decision: {recommendation}")
    print(f"Risk Score:        {result['risk_score']:.2f}")
    print(f"Policy:            {result['policy']}")
    print(f"Proof Hash:        {result['proof_hash']}")

    if recommendation == "APPROVE":
        print("\nProceed with on-chain disbursement.")
    elif recommendation == "REVIEW":
        print("\nEscalate to multisig review before disbursement.")
    else:
        print("\nDisbursement blocked by policy.")

except TrustOSError as e:
    print(f"Treasury verification failed [{e.status_code}]: {e}")
