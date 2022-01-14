from forta_agent import Finding, FindingType, FindingSeverity
from .constants import (
    MY_ADDRESS,
    HACK_ME_CALL_PAUSE_FUNCTION_ABI,
)

with open("./src/address.txt", "r") as file:
    HACK_ME_CONTRACT_ADDRESS = file.read()
file.close()


def handle_transaction(transaction_event):
    findings = []

    # filter transaction info for HackMe function call
    hackme_sensitive_function_invocations = transaction_event.filter_function(
        HACK_ME_CALL_PAUSE_FUNCTION_ABI, HACK_ME_CONTRACT_ADDRESS
    )

    # fire alerts for each function call
    for invocation in hackme_sensitive_function_invocations:
        sender = transaction_event.from_

        findings.append(
            Finding(
                {
                    "name": "Sensitive function call",
                    "description": f"Function called by {sender}",
                    "alert_id": "FORTA",
                    "type": FindingType.Suspicious,
                    "severity": get_severity(sender),
                    "metadata": {
                        "from": transaction_event.from_,
                        "to": transaction_event.to,
                    },
                }
            )
        )
    return findings


def get_severity(sender):
    if sender == MY_ADDRESS:
        return FindingSeverity.Medium
    else:
        return FindingSeverity.Critical
