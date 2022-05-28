// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount)
        external
        returns (bool);

    function allowance(address owner, address spender)
        external
        view
        returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}

contract DefiBank {
    // Deposit
    // WithDraw
    // IssueInterest
    address public usdc;
    address public ausd;

    address[] public stakers;

    mapping(address => uint256) public depositBalance;
    mapping(address => bool) public hasDeposited;

    constructor(address _usdc, address _ausd) {
        usdc = _usdc;
        ausd = _ausd;
    }

    function depositToken(uint256 _amount) public {
        IERC20(usdc).transferFrom(msg.sender, address(this), _amount);
        depositBalance[msg.sender] += _amount;

        if (!hasDeposited[msg.sender]) {
            stakers.push(msg.sender);
        }

        hasDeposited[msg.sender] = true;
    }

    function withdraw(uint256 _amount) public {
        uint256 balance = depositBalance[msg.sender];
        require(balance > 0, "Balance cannot be 0");
        IERC20(usdc).transfer(msg.sender, _amount);

        depositBalance[msg.sender] -= _amount;

        if (balance - _amount == 0) {
            hasDeposited[msg.sender] = false;
        }
    }

    function issueInterest() public {
        for (uint256 i; i < stakers.length; i++) {
            address recipient = stakers[i];
            uint256 balance = depositBalance[recipient];

            if (balance > 0) {
                IERC20(ausd).transfer(recipient, balance);
            }
        }
    }
}
