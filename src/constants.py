MY_ADDRESS = ""
NON_OWNER_ADDRESS = ""
HACK_ME_CALL_PAUSE_FUNCTION_ABI = '{"inputs":[],"name":"callSensitiveFunction","outputs":[],"stateMutability":"nonpayable","type":"function"}'
HACK_ME_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor",
        "name": "constructor",
    },
    {
        "inputs": [],
        "name": "callSensitiveFunction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "sensitiveVar",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "vulnerableFunction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
