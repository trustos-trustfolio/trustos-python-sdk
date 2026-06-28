"""AI agent action verification example.

Verifies a high-impact tool call from an autonomous agent before execution.
Prevents unintended database writes, API calls, or financial operations.
"""

from trustos import TrustOSClient, TrustOSError

client = TrustOSClient()

agent_action = {
    "action": "execute_tool",
    "destination": "database_write",
    "source": "agent-framework",
    "priority": "High",
    "metadata": {
        "tool": "write_record",
        "table": "transactions",
        "agent_id": "agent_alpha_001",
    },
}

try:
    result = client.verify_decision(agent_action)

    if result["recommendation"] == "APPROVE":
        print(f"✅ Agent action approved [{result['decision_id']}]")
        print(f"   Risk Level: {result['risk_level']} — proceeding.")
    elif result["recommendation"] == "REVIEW":
        print("⏳ Agent action requires human review before execution.")
        print(f"   Decision ID: {result['decision_id']}")
        print("   Route to human-in-the-loop queue.")
    else:
        print("❌ Agent action denied by Trust OS policy.")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Risk Score: {result['risk_score']:.2f}")

except TrustOSError as e:
    print(f"Agent verification failed [{e.status_code}]: {e}")
