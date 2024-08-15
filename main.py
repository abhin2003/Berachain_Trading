from web3 import Web3
import json
import queue
import requests
import time

# bera chain end point: https://chainlist.org/chain/80084
#Bits bear tocken: https://etherscan.io/token/0x32bb5a147b5371fd901aa4a72b7f82c58a87e36d#code
#berchain doc: https://docs.berachain.com/
#Example for trading : https://github.com/LaDoger/UniBot/blob/main/washbot.py
# Important for external BEX protocol: https://docs.bex.berachain.com/learn/guides/external-routers


bera_testnet_url="https://bera-testnet.nodeinfra.com"
web3=Web3(Web3.HTTPProvider(bera_testnet_url))
print(Web3.is_connected)

trade_queue = queue.Queue() # for trading

def add_trade_to_queue(trade):
    trade_queue.put(trade)


def get_current_gas_price():
    return web3.eth.gas_price

def get_client(account_number, private_key, proxy, email_address=None, email_password=None) -> Client:
    return Client(account_number, private_key, proxy, email_address, email_password)    

async def swap_bex(account_number, private_key, proxy, *_, **kwargs):
    worker = BeraChain(get_client(account_number, private_key, proxy))
    return await worker.swap_bex(**kwargs)



    async def swap_bex(self, swapdata:dict = None):

        from_token_name, to_token_name, amount, amount_in_wei = swapdata

        self.logger_msg(*self.client.acc_info, msg=f'Swap on BEX: {amount} {from_token_name} -> {to_token_name}')

        token_data = TOKENS_PER_CHAIN[self.network]

        native_address = token_data['BERA'].lower()
        from_token_address = token_data[from_token_name]
        to_token_address = token_data[to_token_name]
        swap_steps = await self.get_swap_steps(from_token_address, to_token_address, amount_in_wei)
        deadline = 99999999
        swap_data = []

        from_token_balance, _, _ = await self.client.get_token_balance(from_token_name, check_symbol=False)

        if from_token_balance >= amount_in_wei:

            if from_token_name != self.client.network.token:
                await self.client.check_for_approved(
                    from_token_address, BEX_CONTRACTS[self.network]['router'], amount_in_wei
                )

            for index, step in enumerate(swap_steps):
                swap_data.append([
                    self.client.w3.to_checksum_address(step["pool"]),
                    self.client.w3.to_checksum_address(step["assetIn"]) if step['assetIn'] != native_address else ZERO_ADDRESS,
                    int(step["amountIn"]),
                    self.client.w3.to_checksum_address(step["assetOut"]),
                    int(int(step["amountOut"]) * 0.95) if index != 0 else 0,
                    "0x"
                ])

            tx_params = await self.client.prepare_transaction(
                value=amount_in_wei if from_token_name == self.client.network.token else 0
            )

            transaction = await self.bex_router_contract.functions.batchSwap(
                0,
                swap_data,
                deadline
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)
        else:
            raise SoftwareException('Insufficient balance on account!')




GAS_PRICE_THRESHOLD = Web3.toWei('20', 'gwei')  # Set your desired gas price threshold

def process_trades():
    while True:
        current_gas_price = get_current_gas_price()

        if current_gas_price < GAS_PRICE_THRESHOLD and not trade_queue.empty():
            trade = trade_queue.get()
            execute_trade(trade, current_gas_price)
        
        time.sleep(10)  # Sleep for 10 seconds before checking again

# Dummy trade execution function
def execute_trade(trade, gas_price):
    print(f"Executing trade {trade} with gas price {gas_price}")
    # Add code to interact with the BEX DEX and execute the trade



trades = ["Trade 1", "Trade 2", "Trade 3"]

    for trade in trades:
        add_trade_to_queue(trade)

    # Start processing trades based on gas price
    process_trades()

abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINT_PRICE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NUM_BABY_BEARS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NUM_BAND_BEARS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NUM_BOND_BEARS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NUM_BONG_BEARS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NUM_BOO_BEARS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"addrs","type":"address[]"}],"name":"airdrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"airdropTokenIDs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimOpen","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"eligibleForClaim","outputs":[{"internalType":"uint256","name":"sum","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fairSaleTokenID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"hasClaimedRebase","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"mintOpen","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
adress="0x32BB5a147b5371Fd901Aa4a72B7F82c58A87e36d"





# $BERA
adress="0x7507c1dc16935B82698e4C63f2746A2fCf994dF8"

#



TOKENS_PER_CHAIN = {
    'BeraChain':{
        'BERA'              : "0x5806E416dA447b267cEA759358cF22Cc41FAE80F",
        'BGT'               : "0xAcD97aDBa1207dCf27d5C188455BEa8a32E80B8b",
        'STGUSDC'           : "0x6581e59A1C8dA66eD0D313a0d4029DcE2F746Cc5",
        'WBTC'              : "0x9DAD8A1F64692adeB74ACa26129e0F16897fF4BB",
        'HONEY'             : "0x7EeCA4205fF31f947EdBd49195a7A88E6A91161B",
        'WETH'              : "0x8239FBb3e3D0C2cDFd7888D8aF7701240Ac4DcA4",
    }
}





contract=web3.eth.contract(address=adress, abi=abi)
print(contract)
print(contract.functions.greet().call())   #Used to call function fromm a smart cotract 
tx_hash= contract.functions.greet().transact()    # used to do transactionon chain 

gas_price=web3.eth.generate_gas_price()
print(gas_price)


account_1= ""
private_key=""

tx={
    'nounce':nouce,
    'to': account_1
    'value': web3.toWei(1,'ether')
    'gas': 200000,
    'gasPrice': web3.toWei('50', 'gwei')
}



signed_tx=web3.eth.account.sign_transaction(tx, private_key)
tx_hash=web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(web3.to_hex(tx_hash))


def swap_tokens(amount_in, token_in_address, token_out_address, recipient_address):
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)

    swap_txn = trade_contract.functions.swap(
        1,  # assuming '1' represents a swap kind
        [
            {
                "poolId": BEX_contract_address,
                "assetIn": token_in_address,
                "amountIn": amount_in,
                "assetOut": token_out_address,
                "amountOut": 0,  # If you're specifying the amount to receive, otherwise 0
                "deadline": web3.eth.getBlock('latest')['timestamp'] + 60 * 15
            }
        ],
        web3.eth.getBlock('latest')['timestamp'] + 60 * 15
    ).buildTransaction({
        'chainId': web3.eth.chain_id,
        'gas': 250000,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.signTransaction(swap_txn, private_key=PRIVATE_KEY)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Swap transaction sent: {txn_hash.hex()}")
    return txn_hash

# Example usage:
amount_in = web3.to_wei(1, 'ether')  # Swap 1 BERA token
swap_tokens(amount_in, BERA_token_address, USDC_token_adress, PUBLIC_KEY)




def place_order(amount, price):
    # Create the transaction dictionary
    transaction = {
        'from': PUBLIC_KEY,
        'gas': 2000000,
        'gasPrice': get_gas_price(),
        'nonce': web3.eth.getTransactionCount(PUBLIC_KEY)
    }
    
    # Build the transaction for the trade
    txn = trade_contract.functions.placeOrder(amount, price).buildTransaction(transaction)
    
    # Sign the transaction with your private key
    signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    
    # Send the signed transaction to the blockchain
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Output the transaction hash
    print(f"Transaction hash: {web3.toHex(txn_hash)}")

# Example trading logic
def trade():
    amount_to_trade = 10  # Amount of tokens to trade (adjust as needed)
    price_to_trade = 100  # Price per token (adjust as needed)
    
    # Fetch the current gas price
    gas_price = get_gas_price()
    print(f"Current gas price: {gas_price}")
    
    # Check if the gas price is below the threshold before trading
    if gas_price < threshold:
        place_order(amount_to_trade, price_to_trade)
    else:
        print("Gas price too high, trade not executed.")

# Run the trade function
trade()




###################################################################################
####################################################################################
###################################################################################
import requests
import json
import queue
from web3 import Web3
from uniswap import Uniswap
from config import BEX_contract_address, BEX_abi, BERA_token_address, BERA_token_abi, USDC_token_address, USDC_token_abi

trade_queue = queue.Queue()

BERACHAIN_TESTNET_URL = "https://bera-testnet.nodeinfra.com"

# Connect to Berachain testnet
web3 = Web3(Web3.HTTPProvider(BERACHAIN_TESTNET_URL))
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Berachain testnet")
else:
    print("Successfully connected to the Berachain testnet")

PRIVATE_KEY = "wing walnut nation area wing truly potato step sunny lazy antique share"
PUBLIC_KEY = "0xE742242A21c9cF853FF6F0B79d69f22C96daa140"

# Create the contract instance
trade_contract = web3.eth.contract(address=BEX_contract_address, abi=BEX_abi)
print(trade_contract)

def get_gas_price():
    gas_price = web3.eth.gas_price  
    print(f"Current gas price: {web3.from_wei(gas_price, 'gwei')} gwei")   # 1 Gwei = 0.000000001 ETH
    return gas_price

def get_token_balance(token_address, wallet_address, token_abi):
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    balance = token_contract.functions.balanceOf(wallet_address).call()
    print(f"Balance of {token_address}: {web3.from_wei(balance, 'ether')} tokens")
    return balance

def trade_tokens(amount, min_out, is_buy, pool_idx):
    gas_price = get_gas_price()
    nonce = web3.eth.get_transaction_count(PUBLIC_KEY)

    # Define the transaction
    tx = {
        'chainId': 1,  # Adjust if needed for testnet
        'to': BEX_contract_address,
        'value': 0,
        'gas': 3000000,
        'gasPrice': gas_price,
        'nonce': nonce,
        'data': trade_contract.encodeABI(
            fn_name='multiSwap',
            args=[[
                {
                    'base': BERA_token_address if is_buy else USDC_token_address,
                    'quote': USDC_token_address if is_buy else BERA_token_address,
                    'poolIdx': pool_idx,
                    'isBuy': is_buy
                }
            ], amount, min_out]
        )
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction hash: {web3.to_hex(tx_hash)}")

    # Wait for the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")

    return tx_receipt

# Example usage
bera_balance = get_token_balance(BERA_token_address, PUBLIC_KEY, BERA_token_abi)
usdc_balance = get_token_balance(USDC_token_address, PUBLIC_KEY, USDC_token_abi)

threshold = Web3.to_wei('20', 'gwei')
print(threshold)

# Example trade
# Assuming you want to buy BERA with USDC
amount_to_trade = Web3.to_wei('10', 'ether')  # Example amount
min_output = Web3.to_wei('5', 'ether')  # Minimum output amount
pool_index = 0  # Specify the pool index

if usdc_balance >= amount_to_trade:
    trade_tokens(amount_to_trade, min_output, True, pool_index)
else:
    print("Insufficient USDC balance for the trade")

##############################################################
###############################################################




import queue
from web3 import Web3
from uniswap import Uniswap
from config import BEX_contract_address, BEX_abi, BERA_token_address, BERA_token_abi, USDC_token_address, USDC_token_abi

trade_queue = queue.Queue()

BERACHAIN_TESTNET_URL = "https://bera-testnet.nodeinfra.com"

# Connect to Berachain testnet
web3 = Web3(Web3.HTTPProvider(BERACHAIN_TESTNET_URL))
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Berachain testnet")
else:
    print("Successfully connected to the Berachain testnet")

PRIVATE_KEY = "wing walnut nation area wing truly potato step sunny lazy antique share"
PUBLIC_KEY = "0xE742242A21c9cF853FF6F0B79d69f22C96daa140"

# Initialize Uniswap
uniswap = Uniswap(address=PUBLIC_KEY, private_key=PRIVATE_KEY, version=2, provider=BERACHAIN_TESTNET_URL)

def get_gas_price():
    gas_price = web3.eth.gas_price  
    print(f"Current gas price: {web3.from_wei(gas_price, 'gwei')} gwei")   # 1 Gwei = 0.000000001 ETH
    return gas_price

def get_token_balance(token_address, wallet_address, token_abi):
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    balance = token_contract.functions.balanceOf(wallet_address).call()
    print(f"Balance of {token_address}: {web3.from_wei(balance, 'ether')} tokens")
    return balance

def trade_tokens(amount, min_out, is_buy):
    gas_price = get_gas_price()
    
    # Amount in smallest unit
    amount_in_wei = Web3.to_wei(amount, 'ether')
    min_out_in_wei = Web3.to_wei(min_out, 'ether')
    
    if is_buy:
        # Trade BERA for USDC
        tx_hash = uniswap.make_trade(BERA_token_address, USDC_token_address, amount_in_wei)
    else:
        # Trade USDC for BERA
        tx_hash = uniswap.make_trade(USDC_token_address, BERA_token_address, amount_in_wei)
    
    print(f"Transaction hash: {web3.to_hex(tx_hash)}")
    
    # Wait for the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")

    return tx_receipt

# Example usage
bera_balance = get_token_balance(BERA_token_address, PUBLIC_KEY, BERA_token_abi)
usdc_balance = get_token_balance(USDC_token_address, PUBLIC_KEY, USDC_token_abi)

threshold = Web3.to_wei('20', 'gwei')
print(threshold)

# Example trade
# Assuming you want to buy BERA with USDC
amount_to_trade = 10  # Example amount in ETH
min_output = 5  # Minimum output amount in ETH

if usdc_balance >= Web3.to_wei(amount_to_trade, 'ether'):
    trade_tokens(amount_to_trade, min_output, True)  # Buy BERA with USDC
else:
    print("Insufficient USDC balance for the trade")



##############################################################################################
#################################################################################################







def swap_tokens(input_token_address, output_token_address, amount, min_output_amount, swap_to):
    gas_price = get_gas_price()
    
    # Amount in smallest unit
    amount_in_wei = Web3.to_wei(amount, 'ether')
    min_output_amount_in_wei = Web3.to_wei(min_output_amount, 'ether')
    
    if swap_to=="USDC":
        tx_hash = uniswap.make_trade(input_token_address, output_token_address, amount_in_wei)
    else:
        tx_hash = uniswap.make_trade(input_token_address, output_token_address, amount_in_wei)
    
    print(f"Transaction hash: {web3.to_hex(tx_hash)}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")



########################################################################################################
########################################################################################################3
########################################################################################################






from web3 import Web3
from config import BEX_contract_address, BEX_abi, BERA_token_address, BERA_token_abi, USDC_token_adress, USDC_token_abi

# Initialize Web3 and the BEX contract
web3 = Web3(Web3.HTTPProvider(BERACHAIN_TESTNET_URL))
private_key = "your-private-key"
public_key = "your-public-key"

# Create the contract instance
bex_contract = web3.eth.contract(address=BEX_contract_address, abi=BEX_abi)

def perform_swap(token_from, token_to, amount, min_out, pool_idx):
    nonce = web3.eth.get_transaction_count(public_key)
    
    # Construct the swap steps
    swap_steps = [
        {
            'base': token_from,
            'quote': token_to,
            'poolIdx': pool_idx,
            'isBuy': True
        }
    ]
    
    # Create the transaction
    transaction = {
        'to': BEX_contract_address,
        'value': 0,
        'gas': 2000000,  # Adjust gas limit as needed
        'gasPrice': web3.to_wei('20', 'gwei'),  # Adjust gas price as needed
        'nonce': nonce,
        'data': bex_contract.encodeABI(fn_name='multiSwap', args=[swap_steps, amount, min_out])
    }

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f"Swap transaction sent: {tx_hash.hex()}")

# Example usage
amount_to_swap = Web3.to_wei(1, 'ether')  # Adjust as needed
min_out = Web3.to_wei(0.5, 'ether')  # Minimum output, adjust as needed
pool_idx = 0  # Pool index, adjust as needed

perform_swap(BERA_token_address, USDC_token_adress, amount_to_swap, min_out, pool_idx)
