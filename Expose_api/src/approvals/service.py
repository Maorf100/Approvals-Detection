import asyncio
from web3 import Web3
from typing import List, Dict, Any
from fastapi import Depends

from .constants import MAX_CONCURRENT_PROCESSES
from .infura_repository import InfuraRepository
from .coin_gecko_repository import CoinGeckoRepository
from .schemas import ApprovalModel

class ApprovalService:
    def __init__(self,
                infura_repository : InfuraRepository = Depends(InfuraRepository),
                coin_gecko_repository : CoinGeckoRepository = Depends(CoinGeckoRepository) ):
        """
        Initialize Service object and repositories for service use
        """
        self.infura_repository = infura_repository
        self.coin_gecko_repository = coin_gecko_repository
        self.semaphore = None 
    
    async def _get_semaphore(self):
        """
        Function returns a Semaphore object used for limiting requests.
        """
        if self.semaphore is None:
            self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_PROCESSES)
        return self.semaphore

    async def get_approvals_by_addresses(self, addresses : List[str]) -> Dict[str, List[ApprovalModel]]:
        """
        Function that takes a list of blockchain addresses and returns their corresponding approvals.

        Parameters:
            addresses (List[str]): List of hexadecimal addresses.

        Returns:
            address_to_approvals (Dict): Dictionary where each key (blockchain address) has a list of approvals they have made.

        """
        semaphore = await self._get_semaphore()
        address_to_approves = {}
        for address in addresses:
            async with semaphore:
                total_approves = await self.infura_repository.get_approvals_by_address(address)
                if total_approves:
                    approvals_list = []
                    
                    for (owner, spender), value in total_approves.items():
                        contract_data = await self.infura_repository.enrich_log_data(owner,spender,value)
                        token_price = await self.coin_gecko_repository.get_token_price(spender)
                        exposure = min(contract_data.balance,value) * token_price if token_price else None
                        approvals_list.append(ApprovalModel(
                            contract_name=contract_data.contract_name,
                            amount=contract_data.approval_amount,
                            token_price= token_price,
                            exposure=exposure
                        ))
                    

                    address_to_approves[address] = approvals_list
                else:
                    return None
        return address_to_approves
    