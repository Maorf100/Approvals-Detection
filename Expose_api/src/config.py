import os
from typing import Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    infura_api_key: str = os.getenv("INFURA_API_KEY", None)
    if not infura_api_key:
       raise ValueError("Infura API Key not provided")
    
    coin_gecko_api_key : str = os.getenv("COIN_GOCKO_API_KEY", None)
    if not coin_gecko_api_key:
        raise ValueError("coin gecko API Key not provided")
        
    

settings = Settings()