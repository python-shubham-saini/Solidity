import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    usdc_contract = Contract('0x9D2aF0199198337e04781cfC5398799F25D0Fd2c')
    defi_contract = Contract('0x426122D719533257B3000c31D25314023D73E755')
    
    print(f"Before function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")
    usdc_contract.approve(defi_contract, 10000, {"from": account})
    defi_contract.depositToken(10000, {"from": account})

    print(f"After function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")
    
    defi_contract.withdraw(100, {"from": account})
    

    print(f"Current balance after Withdraw usdc token deposit balance is {defi_contract.depositBalance(account)}")
