import logging

import fastapi

from netflix_mock.schemas.ef_ir import ProvCustomerData, Forbidden

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


@router.put("/{any_path:path}/{charging_id}")
async def put(
    any_path: str,
    charging_id: str,
    data: ProvCustomerData,
):
    logger.info("PUT >> sub_path=%s, charging_id=%s, data=%s", any_path, charging_id, data)
    return Forbidden(message="I don't know why")


@router.delete("/{any_path:path}/{charging_id}")
async def delete(
    any_path: str,
    charging_id: str,
):
    logger.info("DELETE >> sub_path=%s, charging_id=%s", any_path, charging_id)
