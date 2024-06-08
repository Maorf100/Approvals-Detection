import requests
from http import HTTPStatus
from fastapi import Depends

from config import Settings
from .dependencies import get_settings

from .constants import TOKEN_PRICE_BASE_URL,USD_CURRENCY_CODE

class CoinGeckoRepository:
    def __init__(self,settings : Settings = Depends(get_settings)):
        self.settings = settings

    async def get_token_price(self,contract_address : str) -> int:
        """
        Function gets token_price from CoinGecko API

            Parameters:
                contract_address (str) : hexadecimal address of contract
            
            Returns:
                The price of the token in USD
        """
        url = TOKEN_PRICE_BASE_URL
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.settings.coin_gecko_api_key
        }
        params = {
            'contract_addresses' : contract_address,
            'vs_currencies' : USD_CURRENCY_CODE
        }

        response = requests.get(url, headers=headers,params=params)

        if response.status_code == HTTPStatus.OK:
            data = response.json()
            price = data.get(contract_address.lower(), {}).get(USD_CURRENCY_CODE, None) #return none if didnt exist
            
            return price
        else:
            raise Exception(f"Error {response.status_code}: {response.reason}")