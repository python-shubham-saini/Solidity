import os
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField
from brownie import accounts, Contract , network
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = "89f90514c14a4b8db379caa8ca00c45e"
network.connect('rinkeby')
usdcAddress = Contract('0x7ade72857DF791FCC8E41A2E2936575C5E9A17C5')
contractOfDefi = Contract('0x7195E17d44644F43879ABE0399181B540D45Ce97')

account = accounts.add(os.getenv("PRIVATE_KEY"))
accounts.add(os.getenv("PRIVATE_KEY1"))
accounts.add(os.getenv("PRIVATE_KEY2"))

class Form(FlaskForm):
    Faccounts = SelectField('Account' , choices = ['0x793B8c38647856Afa79675257CE9D75d98DB510b'
                                                    ])
@app.route('/AddFund', methods =["GET", "POST"])
def AddFund():
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        FromAddress = accounts.at(FromAddress, force=True)
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type = int)
        usdcAddress.transfer(ToAddress, Amount * 10 ** 18, {"from": FromAddress})
    return render_template('AddFund.html')

@app.route('/btnfordeposit', methods =['GET', 'POST'])
def btnfordeposit():
    form = Form()
    if request.method == 'POST':
        AmountForDeposit = request.form.get("depositValue", type = int) * (10 ** 18)
        depositBal(AmountForDeposit)
        AmountDeposited = contractOfDefi.depositBalance(account) / (10 ** 18)
        balanceInAccount = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('depositWithdraw.html',form = form,  balanceInAccount = balanceInAccount, AmountDeposited = AmountDeposited)


@app.route('/')
def index():
    # return "<h1>Home page</h1>"
    return render_template('index.html')

def withdrawBal_SC(AmountWithdraw):
    contractOfDefi.withdraw(AmountWithdraw, {"from": account})

def getAccountbal():
    balance = usdcAddress.balanceOf(account)
    return balance

def depositBal(AmountForDeposit):
    usdcAddress.approve(contractOfDefi, AmountForDeposit, {"from": account})
    contractOfDefi.depositToken(AmountForDeposit, {"from": account})

@app.route('/depositWithdraw')
def depositWithdraw():
    form = Form()
    balanceInAccount = getAccountbal() / 10 ** 18
    AmountDeposited = contractOfDefi.depositBalance(account) / (10 ** 18)
    return render_template('depositWithdraw.html', form = form, balanceInAccount = balanceInAccount, AmountDeposited = AmountDeposited)


@app.route('/withdraw_btn', methods =['GET', 'POST'])
def withdraw_btn():
    form = Form()
    if request.method == 'POST':
        AmountWithdraw = request.form.get("withdrawValue", type = int) * (10 ** 18)
        withdrawBal_SC(AmountWithdraw)
        AmountDeposited = contractOfDefi.depositBalance(account) / (10 ** 18)
        balanceInAccount = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('depositWithdraw.html',form = form,  balanceInAccount = balanceInAccount, AmountDeposited = AmountDeposited)

@app.route('/refresh/<currentAccount>')
def refresh(currentAccount):
    global account
    account = accounts.at(currentAccount)
    currentbalance = usdcAddress.balanceOf(account) /(10 ** 18)
    stakedBalance = contractOfDefi.depositBalance(account) / (10 ** 18)
    return jsonify({'response' : currentAccount ,'stakedBalance' : stakedBalance , 'currentbalance': currentbalance})



if __name__ == "__main__":
    
    app.run()
    network.disconnect()