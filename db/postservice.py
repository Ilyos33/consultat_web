from typing import Union, Optional, Dict

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db import get_db

from db.models import Worker_post, Worker


def register_worker_db(worker_name, phone_number, password, email):
    with next(get_db()) as db:
        new_user = Worker(worker_name=worker_name, phone_number=phone_number, password=password, email=email)
        db.add(new_user)
        db.commit()
        return True


def get_all_worker_db():
    with next(get_db()) as db:
        all_users = db.query(Worker).all()
        return all_users


def get_exact_worker_db(user_id):
    with next(get_db()) as db:
        exact_user = db.query(Worker).filter_by(id=user_id).first()
        if exact_user:
            return exact_user
        return False


def delete_exact_worker_post(worker_id):
    with next(get_db()) as db:
        ex_del_user = db.query(Worker).filter_by(id=worker_id).first()
        if ex_del_user:
            db.delete(ex_del_user)
            db.commit()
            return True
        return False


def update_worker_db(worker_id, change_info, new_info):
    with next(get_db()) as db:
        exact_user = db.query(Worker).filter_by(id=worker_id).first()
        if exact_user:
            if change_info == "worker_name":
                exact_user.worker_name = new_info
            elif change_info == "email":
                exact_user.email = new_info
            elif change_info == "phone_number":
                exact_user.phone_number = new_info
            elif change_info == "password":
                exact_user.password = new_info
            db.commit()
            return True
        return False


def check_worker_status_db(worker_id: int) -> Dict[str, Union[str, bool]]:
    try:
        with next(get_db()) as db:
            exact_worker = db.query(Worker_post).filter_by(id=worker_id).first()

            if not exact_worker:
                return {
                    "success": False,
                    "error": f"Пост работника с id {worker_id} не найден"
                }

            return {
                "success": True,
                "is_available": exact_worker.status,
                "message": (
                    "Работник свободен и готов принять заказ"
                    if exact_worker.status
                    else "Работник сейчас занят"
                )
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


def add_worker_post(worker_name: str, phone_number: str, main_text: str, status: bool):
    with next(get_db()) as db:
        new_post = Worker_post(worker_name=worker_name,
                               phone_number=phone_number, main_text=main_text,
                               status=status)
        db.add(new_post)
        db.commit()
        return True


def get_exact_worker_post_db(worker_id):
    with next(get_db()) as db:
        exact_user = db.query(Worker_post).filter_by(id=worker_id).first()
        if exact_user:
            return exact_user
        return False


def all_worker_post_db():
    with next(get_db()) as db:
        exact_user = db.query(Worker_post).all()
        if exact_user:
            return exact_user
        return False


def update_worker_post_db(
        worker_id: int,
        change_info: str,
        new_info: Union[str, bool],
        db: Session = next(get_db())
) -> tuple[bool, Optional[str]]:
    # Словарь допустимых полей и их валидаторов
    valid_fields = {
        "worker_name": lambda x: isinstance(x, str) and len(x.strip()) > 0,
        "phone_number": lambda x: isinstance(x, str) and x.replace('+', '').isdigit(),
        "status": lambda x: isinstance(x, (bool, str)) and (
                isinstance(x, bool) or x.lower() in ['true', 'false']
        ),
        "main_text": lambda x: isinstance(x, str)
    }

    try:
        # Проверяем существование поля
        if change_info not in valid_fields:
            return False, f"Invalid field: {change_info}"

        # Валидируем новое значение
        if not valid_fields[change_info](new_info):
            return False, f"Invalid value for {change_info}"

        with db:
            # Проверяем существование записи
            exact_post = db.query(Worker_post).filter_by(id=worker_id).first()
            if not exact_post:
                return False, f"Worker post with id {worker_id} not found"

            if change_info in ['worker_name', 'phone_number']:
                worker_exists = db.query(Worker).filter(
                    getattr(Worker, change_info) == new_info
                ).first()
                if not worker_exists:
                    return False, f"Referenced worker {change_info} does not exist"

            # Преобразуем str значение в boolean для поля status
            if change_info == 'status':
                if isinstance(new_info, str):
                    new_info = new_info.lower() == 'true'

            # Обновляем значение
            setattr(exact_post, change_info, new_info)
            db.commit()

            return True, None

    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        db.rollback()
        return False, f"Unexpected error: {str(e)}"


def delete_exact_worker_post_db(worker_post_id: int) -> tuple[bool, Optional[str]]:
    try:
        with next(get_db()) as db:
            ex_del_post = db.query(Worker_post).filter_by(id=worker_post_id).first()

            if not ex_del_post:
                return False, f"Worker post with id {worker_post_id} not found"

            db.delete(ex_del_post)
            db.commit()
            return True, None

    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        db.rollback()
        return False, f"Unexpected error: {str(e)}"
