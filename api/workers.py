from fastapi import APIRouter
from db.postservice import *
from pydantic import BaseModel
from typing import Optional
import re

regex = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
worker_router = APIRouter(prefix="/workers",tags=["Работники"])

def check_email(email):
    if re.fullmatch(regex,email):
        return True
    return False


class Workers(BaseModel):
    worker_name:str
    phone_number:str
    password: str
    email: str


@worker_router.post("/register_worker")
async def register_user_api(worker_data:Workers):
    user_db = dict(worker_data)
    mail_validation = check_email(worker_data.email)
    if mail_validation:
        result = register_worker_db(**user_db)
        return result
    return "Ошибка при заполнении почты"


@worker_router.post('/register_worker')
async def reg_user_api(worker_data:Workers):
    worker_db = dict(worker_data)
    mai_validation = check_email(worker_data.email)
    print(mai_validation)
    if mai_validation:
        result = register_worker_db(**worker_db)
        return {"status":1,"message":"Пользователь успешно дрбвлен"}
    return {"status":0,"message":"Неправильный email"}


@worker_router.get("/get_exact_worker")
async def get_exact_worker_api(worker_id:int):
    result = get_exact_worker_db(worker_id)
    return result

@worker_router.get("/get_all_worker")
async def get_all_worker_api():
    return get_all_worker_db()

@worker_router.put("/update_worker_info")
async def update_worker_aoi(worker_id:int,change_info:str,new_info:str):
    resylt = update_worker_db(change_info=change_info,new_info=new_info,worker_id=worker_id)
    if resylt:
        return "Данные сохранены"
    return resylt


@worker_router.delete("/delete_exact_worker")
async def delete_exact_worker_api(worker_id:int):
    return delete_exact_worker_post(worker_id)

@worker_router.delete("/delete_all_worker")
async def delete_all_worker_api(worker_id:int):
    return delete_all_worker()

