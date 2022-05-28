import os
from brownie import accounts, USDC, AUSD, DefiBank
from dotenv import load_dotenv
load_dotenv()


def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    print("account--->",account)
    # account = str("dae765e4321bd1cad0866dae9537f9fe3bddd724ddd0b3c5e7382eeea54a58a6")
    usdc_addr = USDC.deploy({"from":account})
    ausd_addr = AUSD.deploy({"from":account})   
    DefiBank.deploy(usdc_addr, ausd_addr, {"from": account})