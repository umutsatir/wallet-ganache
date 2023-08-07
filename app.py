from web3 import Web3, Account
from solcx import compile_standard
import streamlit as st
import os
from dotenv import load_dotenv
from bip44 import Wallet

## pip install -r reguirements.txt

## it might not be suitable for your folder path, change it accordingly
current_user_file = "current_user.txt"
accounts_file = "accounts.txt"

with open(accounts_file, "r") as file:
    wallets = {}
    i = 0
    for line in file:
        key, value1, value2 = line.split()
        wallets[key] = [value1, value2]
        i += 1

with open(current_user_file, "r") as file:
    current_user = file.read()

load_dotenv()
ganache_ip = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_ip))

print(w3.is_connected())

wallet_count = len(w3.eth.accounts)

## create wallet, login, logout, send transaction, check balance, delete wallet
## next updates: check transaction history


def generate_account(index):
    mnemonic = os.getenv("MNEMONIC")
    wallet = Wallet(mnemonic)
    private, public = wallet.derive_account("eth", account=index)
    account = Account.from_key(private)
    return account


def create_account(w3, username, password):
    global i
    if i < wallet_count:
        if user_exists(username):
            st.warning("User already exists", icon="⚠️")
            return
        else:
            wallets[w3.eth.accounts[i]] = [username, password]
            with open(accounts_file, "a") as file:
                file.write(w3.eth.accounts[i] + " " + username + " " + password + "\n")
            i += 1
            st.success("Wallet created", icon="👛")
            return w3.eth.accounts[i - 1]
    else:
        st.warning("No more wallets available", icon="⚠️")


def user_exists(username):
    for wallet in wallets:
        if username == wallets[wallet][0]:
            return True
    return False


def clear_file(file):
    open(file, "w").close()


def login(username, password):
    for wallet in wallets:
        if username == wallets[wallet][0] and password == wallets[wallet][1]:
            st.success("Logged in", icon="🔓")
            return wallet


def send_transaction(w3, sender, receiver, amount):
    amount = w3.to_wei(amount, "ether")
    w3.eth.send_transaction(
        {
            "from": sender,
            "to": receiver,
            "value": amount,
            "gas": 2000000,
            "gasPrice": w3.to_wei("50", "gwei"),
        }
    )


st.title("Blockchain Wallet")

## sidebar
st.sidebar.caption("*Create a new account or login to an existing one*")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Create Account"):
    if user_exists(username):
        st.warning("User already exists", icon="⚠️")
    else:
        current_user = create_account(w3, username, password)
        with open(current_user_file, "a") as file:
            file.write(current_user)
elif st.sidebar.button("Login"):
    if st.sidebar.button("Logout"):
        current_user = ""
        clear_file(current_user_file)
        st.warning("Logged out", icon="🔒")
    if current_user != "":
        st.warning("Already logged in", icon="⚠️")
    elif username == "" or password == "":
        st.warning("Username and password cannot be empty", icon="⚠️")
    elif not user_exists(username):
        st.warning("User does not exist", icon="⚠️")
    else:
        current_user = login(username, password)
        if current_user != "":
            with open(current_user_file, "a") as file:
                file.write(current_user)
elif st.sidebar.button("Logout"):
    if current_user == "":
        st.warning("Already logged out", icon="⚠️")
    else:
        current_user = ""
        clear_file(current_user_file)
        print("Logged out")
        st.success("Logged out", icon="🔒")
st.sidebar.divider()
## sidebar end

## these show up only if logged in
if current_user != "":
    st.write(f"Hello **{wallets[current_user][0]}**")
    st.write(
        "Current balance: ",
        w3.from_wei(w3.eth.get_balance(current_user), "ether"),
        "ETH",
    )
    if st.sidebar.button("Show public key"):
        st.sidebar.caption(current_user)
    if st.sidebar.button("Show private key"):
        print(wallets[current_user][0])
        # st.sidebar.caption("DISCLAIMER: DO NOT SHARE YOUR PRIVATE KEY WITH ANYONE")
        # st.sidebar.caption(f":red[{current.user}]")  ## ! not working

## send transaction section
st.divider()
st.title("Send transaction")
receiver = st.text_input("Receiver")
amount = st.number_input("Amount")

if st.button("Send"):
    if current_user == "":
        st.warning("Please log in to send transactions", icon="⚠️")
    elif amount <= 0:
        st.warning("Invalid amount!", icon="⚠️")
    elif receiver == "":
        st.warning("Receiver cannot be empty!", icon="⚠️")
    else:
        send_transaction(w3, current_user, receiver, amount)
        st.success("Transaction sent", icon="💸")
