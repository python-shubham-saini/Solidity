import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    contractOfUsdc = Contract('0x9D2aF0199198337e04781cfC5398799F25D0Fd2c')
    contractOfDefi = Contract('0x426122D719533257B3000c31D25314023D73E755')
    
    print(f"This is Fresh USDC token deposit balance  {contractOfDefi.depositBalance(account)}")
    contractOfUsdc.approve(contractOfDefi, 10000, {"from": account})
    contractOfDefi.depositToken(10000, {"from": account})

    print(f"After Deposit token, usdc token deposit balance is {contractOfDefi.depositBalance(account)}")
    
    contractOfDefi.withdraw(100, {"from": account})
    

    print(f"After Withdraw, usdc token deposit balance is {contractOfDefi.depositBalance(account)}")
