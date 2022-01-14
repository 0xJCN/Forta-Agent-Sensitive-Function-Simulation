# Sensitive Function Agent Simulation

## Description

**This agent is not intended for production.**

This agent will scan transactions on the rinkeby testnet and emit alerts for a specific function call to a custom contract that we deploy.
This agent is only intended for educational purposes and I made this repository to learn about forta agent development.

This agent will emit two types of alerts:
1. Medium severity: When the owner of the contract (you) call the sensitive function
2. Critical severity: When a non owner calls the sensitive function (your second address acting as a bad actor).

This repo is supposed to simulate the following situation:
There is a contract that has a sensitive function that should only be called by the owner when the contract functionality needs to altered (should rarely be called). The sensitive function has an onlyOwner modifier so only the owner of the contract should be able to call said function. This contract also has a vulnerable function that allows anyone to become the new owner. That new owner can then call the sensitive function and alter the functionality of the contract. In the wild the attack vector in the contract will be much more complicated, but for simplicity the vulnerable function is simply a function that sets msg.sender to the owner. For this same reason, the sensitive function in our contract simply increments a state variable.


## Setup

You will need to use two ethereum addresses to execute the necessary scripts. You will paste your addresses in `./src/constants.py` for the variables `MY_ADDRESS` and `NON_OWNER_ADDRESS`. You will also need to put your private keys for those addresses in a .env file:
```
# this will be the owner address
export PRVATE_KEY1 ="[Private_key]"
# this will be non owner address
export PRVATE_KEY2 ="[Private_key]"
``` 
**the transaction_event object returns non checksum addresses, therefore your address for the `MY_ADDRESS` variable must be a non checksum address (lower case)**

You will also need to get an RPC URL for Rinkeby testnet. I suggest Alchemy. You will then paste that url in the first line of the forta.config.json file:
```
{
  "jsonRpcUrl": "[YOUR-URL]",                      /* JSON-RPC url for running agent during development e.g. wss://mainnet.infura.io/ws/v3/YOUR_API_KEY */
  // "imageRepositoryUrl": "",              /* Container image repository for publishing agent images */
  // "imageRepositoryUsername": "",         /* Image repository username for authentication, if required */
  // "imageRepositoryPassword": "",         /* Image repository password for authentication, if required */
  // "agentRegistryContractAddress": "",    /* Contract address for agent registry */
  // "agentRegistryJsonRpcUrl": "",         /* JSON-RPC url of the network hosting agent registry contract */
  // "ipfsGatewayUrl": "",                  /* IPFS gateway API for publishing agent manifest e.g. https://ipfs.infura.io:5001 */
  // "ipfsGatewayAuth": "",                 /* Authorization header, if IPFS gateway requires it */
  // "debug": true                          /* Debug flag for additional console logging */
  // "traceRpcUrl": ""                      /* JSON-RPC url for fetching trace data during development */
}
```

## Running simulation

You will do three things to see your agent report the two alerts listed in the `Description`.

1. Run the deploy.py script: **make sure script completes (wait for output) before executing step 3**
2. Run the following command in a separate terminal window: `npm start`
3. Run the send_txs.py script

You will now monitor the output in the terminal window from step 2. It will take a couple of blocks, but you will see your agent report a medium severity alert (function call from the owner) and then it will report a critical severity alert (non owner has exploited contract and called sensitive function).

You can also run the unit tests in `agent_test.py` with the following command: `npm test`

