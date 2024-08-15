import requests
import json
import queue
from web3 import Web3
from config import DEX_contract_address, DEX_abi, HONEY_token_address, HONEY_token_abi, USDC_token_address, USDC_token_abi

trade_queue = queue.Queue()

PRIVATE_KEY = "wing walnut nation area wing truly potato step sunny lazy antique share"
PUBLIC_KEY = "0xE742242A21c9cF853FF6F0B79d69f22C96daa140"
BERACHAIN_TESTNET_URL = "https://bera-testnet.nodeinfra.com"

# Connect to Berachain testnet
web3 = Web3(Web3.HTTPProvider(BERACHAIN_TESTNET_URL))
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Berachain testnet")
else:
    print("Successfully connected to the Berachain testnet")

# Create the contract instances
dex_contract = web3.eth.contract(address=DEX_contract_address, abi=DEX_abi)
print(dex_contract)

USDC_contract = web3.eth.contract(address=USDC_token_address, abi=USDC_token_abi)
print(USDC_contract)

HONEY_contract = web3.eth.contract(address=HONEY_token_address, abi=HONEY_token_abi)
print(HONEY_contract)

def get_gas_price():
    gas_price = web3.eth.gas_price  
    print(f"Current gas price: {web3.from_wei(gas_price, 'gwei')} gwei")
    return gas_price

def get_token_balance(token_address, wallet_address, token_abi):
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    balance = token_contract.functions.balanceOf(wallet_address).call()
    print(f"Balance of {token_address}: {web3.from_wei(balance, 'ether')} tokens")
    return balance

gas_price = get_gas_price()

honey_balance = get_token_balance(HONEY_token_address, PUBLIC_KEY, HONEY_token_abi)
usdc_balance = get_token_balance(USDC_token_address, PUBLIC_KEY, USDC_token_abi)

threshold = web3.to_wei('1158125.1', 'gwei')
print(threshold)

def swap_usdc(amount):
    steps_read = [
        {
            "poolIdx": 36000,
            "base": Web3.to_checksum_address('0x7507c1dc16935b82698e4c63f2746a2fcf994df8'),
            "quote": Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c'),
            "isBuy": True
        }
    ]
    amount_read = web3.to_wei(amount, 'ether')
    output = dex_contract.functions.previewMultiSwap(steps_read, amount_read).call()
    _minOut = int(output[0] * 0.9 * amount_read)
    bear_address_checksum = Web3.to_checksum_address('0x0000000000000000000000000000000000000000')
    quote_address_checksum = Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c')
    _steps = [
        {
            "poolIdx": 36000,  # Example value
            "base": bear_address_checksum,  # ETH address (zero address)
            "quote": quote_address_checksum,  # USDC contract address
            "isBuy": True,
        }
    ]
    tx = {
        'nonce': web3.eth.get_transaction_count(PUBLIC_KEY),
        'chainId': web3.eth.chain_id,
        'gasPrice': int(web3.eth.gas_price * 1.1),
        'gas': 2000000,
        'value': amount_read
    }
    info = dex_contract.functions.multiSwap(_steps, amount_read, _minOut)
    txn = info.build_transaction(tx)
    signed_tx = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Trade executed. Tx hash: {tx_hash.hex()}")

if gas_price < threshold:
    swap_usdc(0.02)
    print("Trade executed")
else:
    print("Gas price too high, trade not executed.")
