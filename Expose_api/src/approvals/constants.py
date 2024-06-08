INFURA_BASE_URL = "https://mainnet.infura.io/v3/"
TOKEN_PRICE_BASE_URL = "https://api.coingecko.com/api/v3/simple/token_price/ethereum"
MAX_UINT_256 = 2**256 - 1
MAX_CONCURRENT_PROCESSES = 3
USD_CURRENCY_CODE = 'usd'

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
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]