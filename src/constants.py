MY_ADDRESS = "0x35184dea3c72c56c7ee9af992a658cc3f671a901"
NON_OWNER_ADDRESS = "0x2aF178C12A65FF16AeEADFa39bA4ade053cc769A"
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
