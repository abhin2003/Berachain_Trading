from web3 import Web3
import json
import queue
import time

# Bera Chain endpoint and contract details
bera_testnet_url = "https://bera-testnet.nodeinfra.com"
web3 = Web3(Web3.HTTPProvider(bera_testnet_url))
print(Web3.is_connected())

trade_queue = queue.Queue()  # Queue for trading

GAS_PRICE_THRESHOLD = Web3.toWei('20', 'gwei')  # Set your desired gas price threshold
print(GAS_PRICE_THRESHOLD)

# Add trade to the queue
def add_trade_to_queue(trade):
    trade_queue.put(trade)

# Get current gas price
def get_current_gas_price():
    return web3.eth.gas_price

# Execute trade when the gas price is below the threshold
def execute_trade(trade, gas_price):
    print(f"Executing trade {trade} with gas price {gas_price}")
    # Add code to interact with the BEX DEX and execute the trade

# Process trades based on gas price
def process_trades():
    while True:
        current_gas_price = get_current_gas_price()

        if current_gas_price < GAS_PRICE_THRESHOLD and not trade_queue.empty():
            trade = trade_queue.get()
            execute_trade(trade, current_gas_price)

        time.sleep(10)  # Sleep for 10 seconds before checking again

# Example usage
trades = ["Trade 1", "Trade 2", "Trade 3"]

for trade in trades:
    add_trade_to_queue(trade)

# Start processing trades based on gas price
process_trades()
