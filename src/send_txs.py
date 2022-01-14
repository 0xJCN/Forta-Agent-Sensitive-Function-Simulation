from forta_agent import get_web3_provider, Web3
from constants import MY_ADDRESS, NON_OWNER_ADDRESS, HACK_ME_ABI
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# get address from txt file
with open("./src/address.txt", "r") as file:
    HACK_ME_CONTRACT_ADDRESS = file.read()
file.close()

# set variables
w3 = get_web3_provider()
hack_me_contract = w3.eth.contract(address=HACK_ME_CONTRACT_ADDRESS, abi=HACK_ME_ABI)
private_key1 = os.getenv("PRIVATE_KEY1")
private_key2 = os.getenv("PRIVATE_KEY2")
chain_id = 4
MY_ADDRESS = w3.toChecksumAddress(MY_ADDRESS)  # Web3.py only accepts checksum addresses
nonce1 = w3.eth.getTransactionCount(MY_ADDRESS)
nonce2 = w3.eth.getTransactionCount(NON_OWNER_ADDRESS)


def send_transactions():
    # build transaction
    pause_tx = hack_me_contract.functions.callSensitiveFunction().buildTransaction(
        {"chainId": chain_id, "from": MY_ADDRESS, "nonce": nonce1}
    )

    # sign transaction
    signed_pause_tx = w3.eth.account.sign_transaction(
        pause_tx, private_key=private_key1
    )

    # send transaction
    send_pause_tx = w3.eth.send_raw_transaction(signed_pause_tx.rawTransaction)

    # wait for transaction
    pause_tx_receipt = w3.eth.wait_for_transaction_receipt(send_pause_tx)


def send_transaction_that_triggers_alert():
    ### call tx that lets you become owner
    # build transaction
    exploit_tx = hack_me_contract.functions.vulnerableFunction().buildTransaction(
        {"chainId": chain_id, "from": NON_OWNER_ADDRESS, "nonce": nonce2}
    )

    # sign transaction
    signed_exploit_tx = w3.eth.account.sign_transaction(
        exploit_tx, private_key=private_key2
    )

    # send transaction
    send_exploit_tx = w3.eth.send_raw_transaction(signed_exploit_tx.rawTransaction)

    # wait for transaction
    exploit_tx_receipt = w3.eth.wait_for_transaction_receipt(send_exploit_tx)

    ### call function that we are monitoring
    # build transaction
    pause_tx = hack_me_contract.functions.callSensitiveFunction().buildTransaction(
        {"chainId": chain_id, "from": NON_OWNER_ADDRESS, "nonce": nonce2 + 1}
    )

    # sign transaction
    signed_pause_tx = w3.eth.account.sign_transaction(
        pause_tx, private_key=private_key2
    )

    # send transaction
    send_pause_tx = w3.eth.send_raw_transaction(signed_pause_tx.rawTransaction)

    # wait for transaction
    pause_tx_receipt = w3.eth.wait_for_transaction_receipt(send_pause_tx)


send_transactions()
print("Owner tx sent...")

send_transaction_that_triggers_alert()
print("Hacker tx sent...")
