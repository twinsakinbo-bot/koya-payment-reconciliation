
#!/usr/bin/env python3
"""Payment reconciliation for Koya."""

import json
from decimal import Decimal

latest_payments = {}

# Read and process payment events
with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(event, dict):
            continue

        txn_id = event.get("txn_id")

        if not txn_id:
            continue

        # Keep only the latest attempt for each transaction
        if (
            txn_id not in latest_payments
            or event["ts"] > latest_payments[txn_id]["ts"]
        ):
            latest_payments[txn_id] = event

# Calculate successful payments
total = Decimal("0")
count = 0

for event in latest_payments.values():
    if event["status"] == "success":
        amount = Decimal(str(event["amount"]).replace(",", ""))
        total += amount
        count += 1

# Verify against the expected count
with open("expected.txt", encoding="utf-8") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count}, expected {expected}.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
