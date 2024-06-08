import argparse
import os
from web3 import Web3

SPENDER_INDEX = 1
MAX_UINT_256 = 2**256 - 1
INFURA_API_KEY = os.getenv("INFURA_API_KEY", None)
INFURA_BASE_URL = 'https://mainnet.infura.io/v3/'

#typically located in external file of config
REQUIRED_EVENTS_ABI = [{
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "owner", "type": "address"},
        {"indexed": True, "name": "spender", "type": "address"},
        {"indexed": False, "name": "value", "type": "uint256"}
    ],
    "name": "Approval",
    "type": "event"
},
{
    "constant": True,
    "inputs": [],
    "name": "decimals",
    "outputs": [
        {
            "name": "",
            "type": "uint8"
        }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
},
{
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "owner",
                "type": "address"
            },
            {
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

if not INFURA_API_KEY:
    raise ValueError("Infura API key not provided")

web3 = Web3(Web3.HTTPProvider(INFURA_BASE_URL + INFURA_API_KEY))

if not web3.is_connected():
    raise ConnectionError("Could not connect to Ethereum node.")

parser = argparse.ArgumentParser(description="Fetch Approval events for given address.")
parser.add_argument('--address', type=str, help='The address you want to query')
args = parser.parse_args()

blockchain_address = args.address

approval_event_signature = web3.keccak(text="Approval(address,address,uint256)").hex()
address_topic = web3.to_hex(web3.to_bytes(hexstr=blockchain_address).rjust(32, b'\0'))

only_approvals_filter_params = {
    'fromBlock': '0x0',
    'toBlock': 'latest',
    'topics': [approval_event_signature, address_topic],
}

# Getting all approve events ever approved by owner
event_logs = web3.eth.filter(only_approvals_filter_params).get_all_entries()

approvals = {}

if event_logs:
    for log in event_logs:
        spender = log['address']
        
        # By this techniqe, owner and spender used as key so repeating approvals 
        # overriden by each other
        approvals[(blockchain_address,spender)] = web3.to_int(log['data'])
        
    # In this loop approval contains tuple of owner and spender
    for approval, value in approvals.items():
        contract = web3.eth.contract(address=approval[SPENDER_INDEX], abi=REQUIRED_EVENTS_ABI)
        contract_name = contract.functions.name().call()
        decimals = contract.functions.decimals().call()
        human_readable_value = "Unlimited" if value == MAX_UINT_256 else value / (10 ** decimals)
        print(f"approval on {contract_name} on amount of {human_readable_value}")
else:
    print("No approval logs found for the given address.")
