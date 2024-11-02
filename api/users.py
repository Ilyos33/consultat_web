from fastapi import APIRouter
from db.userservice import *
from pydantic import BaseModel
from typing import Optional
import re


user_router = APIRouter(prefix="/user",tags=["Пользователи"])
regex = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")


def check_ph_num(phone_number):
    if re.fullmatch(regex,phone_number):
        return True
    return False

regex1 = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
def check_email(email):
    if re.fullmatch(regex1,email):
        return True
    return False



class Users(BaseModel):
    user_name:str
    phone_number:str
    password: str
    email: str

@user_router.post("/register_user")
async def register_user_api(user_data: Users):
    user_db = dict(user_data)
    mail_validation = check_email(user_data.email)
    if mail_validation:
        result = register_user_db(**user_db)
        return result
    return "Ошибка при заполнении почты"

@user_router.get("/log_in")
async  def login_user_db(login, password):
    with next(get_db()) as db:
        user_by_phone = db.query(User).filter_by(phone_number=login).first()
        user_by_email = db.query(User).filter_by(email=login).first()
        if user_by_phone:
            if user_by_phone.password == password:
                return user_by_phone.id
        elif user_by_email:
            if user_by_email.password == password:
                return user_by_email.id
        return "Неправильные данные"


@user_router.get("/get_exact_user")
async def get_exact_user_api(user_id:int):
    result = get_exact_user_db(user_id)
    return result

@user_router.get("/get_all_users")
async def get_all_users_api():
    return get_all_users_db()

@user_router.put("/update_user_info")
async def update_user_aoi(user_id:int,change_info:str,new_info:str):
    result = update_user_db(user_id, change_info, new_info)
    if result:
        return "Данные сохранены"
    return result


@user_router.delete("/delete_user")
async def delete_user_api(user_id:int):
    return delete_exact_user(user_id)

@user_router.delete("/delete_all")
async def del_all_user_api():
    return delete_all_user()