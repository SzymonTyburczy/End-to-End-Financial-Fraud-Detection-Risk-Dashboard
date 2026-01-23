# src/rules.py
from typing import Optional, Dict

class FraudRulesEngine:
    def __init__(self):
        pass

    def check_hard_rules(self, transaction_data: dict) -> Optional[Dict]:
        """
        Checks rules.
        Returns a dictionary with a FRAUD result if the rule was broken.
        Returns None if the transaction passed the tests (and can be fed into the AI model).
        """
        amount = transaction_data.get("amount", 0)
        old_balance = transaction_data.get("oldbalanceOrg", 0)
        txn_type = transaction_data.get("type", "")

        if amount <= 0:
            return {
                "prediction": "FRAUD",
                "fraud_probability": 1.0,
                "details": "Hard Rule: Invalid Amount (<=0)"
            }

        if amount > old_balance:
            return {
                "prediction": "FRAUD",
                "fraud_probability": 1.0,
                "details": f"Hard Rule: Insufficient Funds ({amount} > {old_balance})"
            }

        if amount > 1_000_000:
            return {
                "prediction": "FRAUD",
                "fraud_probability": 1.0,
                "details": "Hard Rule: Transaction limit exceeded (>1M)"
            }

        return None