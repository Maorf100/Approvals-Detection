import asyncio
from fastapi import FastAPI ,status,APIRouter,Query,Depends
from pydantic import BaseModel
from typing import List, Dict, Any

from .schemas import ApprovalsResponseModel,ApprovalModel
from .service import ApprovalService

router = APIRouter()

@router.get(
    "/approvals",
    response_model=ApprovalsResponseModel,
    status_code=status.HTTP_200_OK,
    description="return approvals of blockchain addresses provided",
    summary="get approvals for provided addresses",
    responses={
        status.HTTP_200_OK: {
            "model": ApprovalsResponseModel, 
            "description": "Ok Response",
        }

    })
async def get_approvals(addresses : List[str] = Query(..., description="List of blockchain addresses"),
                         service : ApprovalService = Depends(ApprovalService)) -> Dict[str, List[ApprovalModel]]:
    return await service.get_approvals_by_addresses(addresses)