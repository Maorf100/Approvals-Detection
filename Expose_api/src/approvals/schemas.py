from pydantic import BaseModel,RootModel,Field
from typing import Dict,List,Optional,Any

class TokenApproval(BaseModel):
    token_name: str = Field(..., description="Name of the token")
    approval_amount: float = Field(..., description="Approval amount of the token")

class ApprovalModel(BaseModel):
    contract_name: str
    amount: Any
    token_price: Optional[float]
    exposure : Optional[float]

class EnrichedModel(BaseModel):
    contract_name: str
    approval_amount: Any
    balance : float

class ApprovalsResponseModel(RootModel):
    root: Dict[str, List[ApprovalModel]]
