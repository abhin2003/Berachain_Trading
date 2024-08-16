import requests
import json
import queue
from web3 import Web3
from config import DEX_contract_adress,DEX_abi,BERA_token_adress,BERA_token_abi,USDC_token_adress,USDC_token_abi

trade_queue = queue.Queue()

PRIVATE_KEY = "754eb2dbc7db5078be142fc0c4742999fbcecd6610a0b1108c1db71af20c154b"
PUBLIC_KEY = "0x7F870265638CC50D08650cd51eB705238D2c8Eb7"
BERACHAIN_TESTNET_URL = "https://bera-testnet.nodeinfra.com"


#COnnect to berachain testnet
web3 = Web3(Web3.HTTPProvider(BERACHAIN_TESTNET_URL))
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Berachain testnet")
else:
    print("Successfully connected to the Berachain testnet")


# DEX contract
trade_contract = web3.eth.contract(address=DEX_contract_adress, abi=DEX_abi)
print(trade_contract)


USDC_contract = web3.eth.contract(address=USDC_token_adress, abi=USDC_token_abi)
print(trade_contract)


HONEY_contract = web3.eth.contract(address=BERA_token_adress, abi=BERA_token_abi)
print(trade_contract)


def get_gas_price():
    gas_price = web3.eth.gas_price  
    print(f"Current gas price: {web3.from_wei(gas_price, 'gwei')} gwei")   #1 Gwei = 0.000000001 ETH
    return gas_price


def get_token_balance(token_address, wallet_address,token_abi):
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    balance = token_contract.functions.balanceOf(wallet_address).call()
    print(f"Balance of {token_address}: {web3.from_wei(balance, 'ether')} tokens")
    return balance

def addtoqueue(amount):
    trade_queue.put(amount)
    print(f"Trade for {amount} USDC is in the queue.")

gas_price = get_gas_price()

bera_balance = get_token_balance(BERA_token_adress, PUBLIC_KEY,BERA_token_abi)
usdc_balance = get_token_balance(USDC_token_adress, PUBLIC_KEY,USDC_token_abi)

threshold = Web3.to_wei('1158125.1', 'gwei')
print(threshold)



def swap_usdc(amount):
    steps_read = [
        {
            "poolIdx": 36000,
            "base": Web3.to_checksum_address('0x7507c1dc16935B82698e4C63f2746A2fCf994dF8'),
            "quote": Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c'),
            "isBuy": True
        }
    ]
    amount_read = web3.to_wei(amount, 'ether')
    output = trade_contract.functions.previewMultiSwap(steps_read, amount_read).call()
    print(output)
    _minOut = int(output[0] * 0.9 * amount_read)
    bear_address_checksum = Web3.to_checksum_address('0x7507c1dc16935B82698e4C63f2746A2fCf994dF8')
    quote_address_checksum = Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c')
    _steps = [
        {
            "poolIdx": 36000,  
            "base": bear_address_checksum,  
            "quote": quote_address_checksum,  
            "isBuy": True,
        }
    ]
    tx = {
        'nonce': web3.eth.get_transaction_count(PUBLIC_KEY),
        'chainId': web3.eth.chain_id,
        'gasPrice': int(web3.eth.gas_price * 1.1),
        'gas': 5000000,
        'value': amount_read
    }
    info = trade_contract.functions.multiSwap(_steps, amount_read, _minOut)
    txn = info.build_transaction(tx)
    signed_tx = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Trade executed. Tx hash: {tx_hash.hex()}")




addtoqueue(0.02)
addtoqueue(0.05)


while not trade_queue.empty():
    if gas_price < threshold:
        amount = trade_queue.get()  
        swap_usdc(amount)
        print("Trade is executed")
    else:
        print("Gas price too high, trade not executed.")






# def get_gas_price():
#     response = requests.get("https://api.berachain.org/gasPrice")
#     return response.json()["gasPrice"]







# # Function to place a trade order
# def place_order(amount, price):
#     transaction = {
#         'from': PUBLIC_KEY,
#         'gas': 2000000,
#         'gasPrice': get_gas_price(),
#         'nonce': web3.eth.getTransactionCount(PUBLIC_KEY)
#     }
    
#     # Build transaction
#     txn = trade_contract.functions.placeOrder(amount, price).buildTransaction(transaction)
    
#     # Sign transaction
#     signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    
#     # Send transaction
#     txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
#     print(f"Transaction hash: {web3.toHex(txn_hash)}")

# # Simple trading logic
# def main():
#     amount_to_trade = 10  # Example amount
#     price_to_trade = 100  # Example price
    
#     # Get current gas price
#     gas_price = get_gas_price()
#     print(f"Current gas price: {gas_price}")

#     # Place a trade order
#     place_order(amount_to_trade, price_to_trade)
