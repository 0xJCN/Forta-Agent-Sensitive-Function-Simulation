from forta_agent import get_web3_provider, Web3
from constants import MY_ADDRESS
from solcx import compile_standard
import os
from dotenv import load_dotenv

load_dotenv()

# read contract
with open("./src/HackMe.sol", "r") as file:
    hack_me_file = file.read()
file.close()

# compile contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"HackMe.sol": {"content": hack_me_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.11",
)

# get bytecode
bytecode = compiled_sol["contracts"]["HackMe.sol"]["HackMe"]["evm"]["bytecode"][
    "object"
]

# get abi
abi = compiled_sol["contracts"]["HackMe.sol"]["HackMe"]["abi"]

# set up web3
w3 = get_web3_provider()

# create contract
HackMe = w3.eth.contract(abi=abi, bytecode=bytecode)


# build transaction
MY_ADDRESS = w3.toChecksumAddress(MY_ADDRESS)  # Web3.py only accepts checksum addresses
private_key = os.getenv("PRIVATE_KEY1")
chain_id = 4
nonce = w3.eth.getTransactionCount(MY_ADDRESS)

tx = HackMe.constructor().buildTransaction(
    {"chainId": chain_id, "from": MY_ADDRESS, "nonce": nonce}
)

# sign transaction
signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)

# send transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait for transaction
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract address: {tx_receipt.contractAddress}")

# get contract
hack_me_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# read owner vairable
print(f"Owner of the contract: {hack_me_contract.functions.owner().call()}")


# write contract address to address.txt
with open("./src/address.txt", "w") as file:
    file.write(tx_receipt.contractAddress)
file.close()
