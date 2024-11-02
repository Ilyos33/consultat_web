from fastapi import APIRouter, HTTPException, status
from db.postservice import *
from pydantic import BaseModel
from typing import Optional, Union

worker_post_router = APIRouter(prefix="/workers", tags=["Посты работников"])


class Worker_post(BaseModel):
    worker_name: str
    phone_number: str
    main_text: str
    status: bool


@worker_post_router.post("/reg_worker_post")
async def reg_worker_post(wk_data: Worker_post):
    wk_data1 = dict(wk_data)
    wk = add_worker_post(**wk_data1)
    return wk


@worker_post_router.get("/get_exact_worker_post")
async def get_exact_worker_post(worker_id):
    return get_exact_worker_post_db(worker_id)


@worker_post_router.get("/get_all_worker_post")
async def get_all_worker_post_api():
    return all_worker_post_db()


@worker_post_router.put("/update_worker_post_info")
async def update_worker_api(
        worker_id: int,
        change_info: str,
        new_info: Union[str, bool]
):
    success, error_message = update_worker_post_db(worker_id, change_info, new_info)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message or "Failed to update worker post"
        )

    return {"message": "Данные успешно сохранены"}


@worker_post_router.delete("/delete_exact_worker_post")
async def delete_exact_worker_post_api(worker_post_id: int):
    success, error_message = delete_exact_worker_post_db(worker_post_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in (error_message or "")
            else status.HTTP_400_BAD_REQUEST,
            detail=error_message or "Failed to delete worker post"
        )

    return {"message": "Пост успешно удален"}


@worker_post_router.get("/chek_status")
async def check_status_api(worker_id: int):
    result = check_worker_status_db(worker_id)

    if not result["success"]:
        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
                if "not found" in result.get("error", "")
                else status.HTTP_400_BAD_REQUEST
            ),
            detail=result["error"]
        )

    return {
        "worker_id": worker_id,
        "is_available": result["is_available"],
        "message": result["message"]
    }
