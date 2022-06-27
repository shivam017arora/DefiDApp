//SPDX-Licence-Identifer: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockWeth is ERC20 {
    constructor() public ERC20("MockWeth", "Weth") {
    }
}