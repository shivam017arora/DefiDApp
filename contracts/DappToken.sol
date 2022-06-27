//SPDX-Licence-Identifer: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DappToken is ERC20 {
    constructor() public ERC20("DappToken", "DApp") {
        _mint(msg.sender, 1000000000000000000000000); //1 Million DApp Tokens
    }
}