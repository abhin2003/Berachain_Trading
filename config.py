from web3 import Web3



#Website : https://bartio.beratrail.io/address/0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D/contract/80084/code

#DEX bera_usdc_pool contract adress

DEX_contract_adress = Web3.to_checksum_address('0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D')         

#DEX router conract abi
DEX_abi = [
  {
    "type": "constructor",
    "inputs": [
      {
        "name": "_crocSwapDex",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "_crocImpact",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "_crocQuery",
        "type": "address",
        "internalType": "address"
      }
    ],
    "stateMutability": "nonpayable"
  },
  {
    "type": "receive",
    "stateMutability": "payable"
  },
  {
    "type": "function",
    "name": "crocSwapDex",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address",
        "internalType": "contract CrocSwapDex"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "multiSwap",
    "inputs": [
      {
        "name": "_steps",
        "type": "tuple[]",
        "internalType": "struct SwapHelpers.SwapStep[]",
        "components": [
          {
            "name": "poolIdx",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "base",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "quote",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "isBuy",
            "type": "bool",
            "internalType": "bool"
          }
        ]
      },
      {
        "name": "_amount",
        "type": "uint128",
        "internalType": "uint128"
      },
      {
        "name": "_minOut",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [
      {
        "name": "out",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "stateMutability": "payable"
  },
  {
    "type": "function",
    "name": "previewMultiSwap",
    "inputs": [
      {
        "name": "_steps",
        "type": "tuple[]",
        "internalType": "struct SwapHelpers.SwapStep[]",
        "components": [
          {
            "name": "poolIdx",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "base",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "quote",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "isBuy",
            "type": "bool",
            "internalType": "bool"
          }
        ]
      },
      {
        "name": "_amount",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [
      {
        "name": "out",
        "type": "uint128",
        "internalType": "uint128"
      },
      {
        "name": "predictedQty",
        "type": "uint256",
        "internalType": "uint256"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "retire",
    "inputs": [],
    "outputs": [],
    "stateMutability": "nonpayable"
  }
]


###########################################################################################
###########################################################################################
#############################################################################################




#website : https://bartio.beratrail.io/address/0x7507c1dc16935B82698e4C63f2746A2fCf994dF8
HONEY_token_adress = Web3.to_checksum_address('0x0E4aaF1351de4c0264C5c7056Ef3777b41BD8e03')
HONEY_token_abi =  [
  {
    "constant": True,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": False,
    "inputs": [
      {
        "name": "spender",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]



#################################################################################
#################################################################################
#################################################################################


USDC_token_adress = Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c')
USDC_token_abi=[
  {
    "constant": True,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": False,
    "inputs": [
      {
        "name": "spender",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]