from fastapi import APIRouter
from db.postservice import *
from pydantic import BaseModel
from typing import Optional

worker_post_router = APIRouter(prefix="/workers",tags=["Посты работников"])

class Worker_post(BaseModel):
    worker_name:str
    phone_number:str
    main_text:str
    status:bool



@worker_post_router.post("/reg_worker_post")
async def reg_worker_post(wk_data:Worker_post):
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
async def update_worker_api(worker_id:int,change_info:str,new_info:str):
    result = update_worker_post_db(change_info, new_info,worker_id)
    if result:
        return "Данные сохранены"
    return result

@worker_post_router.delete("/delete_exact_worker_post")
async def delete_exact_worker_post_api(worker_id):
    return delete_exact_worker_post(worker_id)


@worker_post_router.get("/chek_status")
async def check_status(worker_id):
    return chek_status(worker_id)



