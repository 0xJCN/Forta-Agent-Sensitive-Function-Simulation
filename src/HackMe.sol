// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

contract HackMe {
    uint256 public sensitiveVar = 0;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function incrementSensitiveVar() internal {
        sensitiveVar++;
    }

    function callSensitiveFunction() public onlyOwner {
        incrementSensitiveVar();
    }

    function vulnerableFunction() public {
        owner = msg.sender;
    }
}
