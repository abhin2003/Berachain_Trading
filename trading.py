import asyncio
from modules import Client


client = Client(network='BeraChain', private_key='YOUR_PRIVATE_KEY')


berachain = BeraChain(client)

async def main():
    
    from_token = 'STGUSDC'  
    to_token = 'HONEY'      
    amount = 1.0            
    
    amount_in_wei = int(amount * 10 ** 18)

    try:
        
        swap_data = {
            'from_token_name': from_token,
            'to_token_name': to_token,
            'amount': amount,
            'amount_in_wei': amount_in_wei
        }
        
        swap_result = await berachain.swap_bex(swap_data)
        print(f'Swap successful: {swap_result}')

    except Exception as e:
        print(f'Error occurred: {e}')

