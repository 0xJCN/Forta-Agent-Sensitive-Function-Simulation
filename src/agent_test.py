from unittest.mock import Mock
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from .agent import handle_transaction
from .constants import (
    NON_OWNER_ADDRESS,
    MY_ADDRESS,
    HACK_ME_CALL_PAUSE_FUNCTION_ABI,
)

# get address from txt file
with open("./src/address.txt", "r") as file:
    HACK_ME_CONTRACT_ADDRESS = file.read()
file.close()

mock_tx_event = create_transaction_event(
    {"transaction": {"from": MY_ADDRESS, "to": HACK_ME_CONTRACT_ADDRESS}}
)
mock_tx_event.filter_function = Mock()


class TestMonitorSensitiveFunctionAgent:
    def test_returns_empty_findings_if_no_function_calls(self):
        mock_tx_event.filter_function.return_value = []

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 0
        mock_tx_event.filter_function.assert_called_once_with(
            HACK_ME_CALL_PAUSE_FUNCTION_ABI, HACK_ME_CONTRACT_ADDRESS
        )

    def test_returns_medium_alert_if_owner_calls_function(self):
        mock_tx_event.filter_function.reset_mock()
        mock_args = {"from": MY_ADDRESS, "to": HACK_ME_CONTRACT_ADDRESS}
        mock_transfer_from_invocation = ({}, mock_args)
        mock_tx_event.filter_function.return_value = [mock_transfer_from_invocation]

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 1
        mock_tx_event.filter_function.assert_called_once_with(
            HACK_ME_CALL_PAUSE_FUNCTION_ABI, HACK_ME_CONTRACT_ADDRESS
        )
        finding = findings[0]
        formatted_sender = mock_args["from"]
        assert finding.name == "Sensitive function call"
        assert finding.description == f"Function called by {formatted_sender}"
        assert finding.alert_id == "FORTA"
        assert finding.severity == FindingSeverity.Medium
        assert finding.type == FindingType.Suspicious
        assert finding.metadata["from"] == mock_args["from"]
        assert finding.metadata["to"] == mock_args["to"]

    def test_returns_critical_alert_if_non_owner_calls_function(self):
        mock_tx_event = create_transaction_event(
            {"transaction": {"from": NON_OWNER_ADDRESS, "to": HACK_ME_CONTRACT_ADDRESS}}
        )
        mock_tx_event.filter_function = Mock()

        mock_args = {"from": NON_OWNER_ADDRESS, "to": HACK_ME_CONTRACT_ADDRESS}
        mock_transfer_from_invocation = ({}, mock_args)
        mock_tx_event.filter_function.return_value = [mock_transfer_from_invocation]

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 1
        mock_tx_event.filter_function.assert_called_once_with(
            HACK_ME_CALL_PAUSE_FUNCTION_ABI, HACK_ME_CONTRACT_ADDRESS
        )
        finding = findings[0]
        formatted_sender = mock_args["from"]
        assert finding.name == "Sensitive function call"
        assert finding.description == f"Function called by {formatted_sender}"
        assert finding.alert_id == "FORTA"
        assert finding.severity == FindingSeverity.Critical
        assert finding.type == FindingType.Suspicious
        assert finding.metadata["from"] == mock_args["from"]
        assert finding.metadata["to"] == mock_args["to"]
