from typing import Dict,Tuple,List,Any
from web3 import Web3
from fastapi import Depends

from config import Settings
from .constants import INFURA_BASE_URL,MAX_UINT_256,REQUIRED_EVENTS_ABI
from .dependencies import get_settings
from .schemas import EnrichedModel

class InfuraRepository:
    def __init__(self, settings : Settings = Depends(get_settings)):
        infura_url = INFURA_BASE_URL + settings.infura_api_key
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        if not self.web3.is_connected():
            raise ConnectionError("Could not connect to Ethereum node.")

    async def get_approvals_by_address(self,owner : str) -> Dict[Tuple[str,str],Any]: 
        """
        Function gets owner address and returns his approvals

            Parameters:
                owner (str) : hexadecimal blockchain address of the owner 
            
            Returns:
                approvals (Dictionary) : dictionary contains (owner,spender) tuple as key 
                and amount of approval as value
        """
        approvals = {}

        approval_event_signature = self.web3.keccak(text="Approval(address,address,uint256)").hex()
        address_topic = self.web3.to_hex(self.web3.to_bytes(hexstr=owner).rjust(32, b'\0'))

        only_approvals_filter_params = {
            'fromBlock': '0x0',
            'toBlock': 'latest',
            'topics': [approval_event_signature, address_topic],
        }

        try:
            event_logs = self.web3.eth.filter(only_approvals_filter_params).get_all_entries()
        except Exception as ex:
            raise RuntimeError(f"Error fetching event logs: {ex}")

        for log in event_logs:
            spender = log['address']
            approvals[(owner,spender)] = self.web3.to_int(log['data'])
        
        return approvals

    async def enrich_log_data(self,owner : str, spender : str, value : int) -> EnrichedModel:
        """
        Function gets contract data and returns enriched model.

            Parameters:
                owner (str)   : Hexadecimal address representing the owner of the token.
                spender (str) : Hexadecimal address representing the spender of the token.
                value (int)   : Value of the approval.
            Returns:
                EnrichedModel: Enriched model containing contract name, approval amount and balance.
        """
        try:
            contract = self.web3.eth.contract(address=spender, abi=REQUIRED_EVENTS_ABI)
            contract_name = contract.functions.name().call()
            balance = contract.functions.balanceOf(owner).call()
            decimals = contract.functions.decimals().call()
            human_readable_value = "Unlimited" if value == MAX_UINT_256 else self.calculate_human_readable_number(value,decimals)
            human_readable_balance = self.calculate_human_readable_number(balance,decimals)
            return EnrichedModel(
                contract_name= contract_name,
                approval_amount=human_readable_value,
                balance=human_readable_balance)
        except Exception as ex:
            raise RuntimeError(f"Error enriching log data: {ex}")

    def calculate_human_readable_number(self, amount : int, decimals : int) -> float:
        """
        Function gets amount and count of decimals and return readable amount
        
            Parameters:
                amount   (int) : the amount we want to be more readable (probebly a very large number)
                decimals (int) : number provied by contract for readablilty purposes
            
            Retruns:
                readable (float) number

        """
        return amount / (10 ** decimals)