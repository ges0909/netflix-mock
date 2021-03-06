import logging

import fastapi

from netflix_mock.schemas.api_error import ApiError
from netflix_mock.schemas.ef_ir import Forbidden, ProvCustomerData

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


@router.put(
    path="/{any_path:path}/{charging_id}",
    response_model=Forbidden,
    responses={
        401: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def create_customer(
    any_path: str,
    charging_id: str,
    data: ProvCustomerData,
):
    logger.info("PUT >> sub_path=%s, charging_id=%s, data=%s", any_path, charging_id, data)
    return Forbidden(message="I don't know why")


@router.delete(
    path="/{any_path:path}/{charging_id}",
    responses={
        401: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def delete(
    any_path: str,
    charging_id: str,
):
    logger.info("DELETE >> sub_path=%s, charging_id=%s", any_path, charging_id)
