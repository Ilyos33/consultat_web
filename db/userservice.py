from db import get_db

from db.models import User

def check_user_db(name, phone_number, email):
    with next(get_db()) as db:
        check_name = db.query(User).filter_by(name=name).first()
        check_phone_number = db.query(User).filter_by(
            phone_number=phone_number).first()
        check_email = db.query(User).filter_by(email=email).first()
        if check_name:
            return "Юзернейм занят"
        if check_phone_number:
            return "Телефон номер занят"
        if check_email:
            return "Почта занята"
        return True
def register_user_db(user_name,phone_number,password,email):
    with next(get_db()) as db:
        new_user = User(user_name=user_name,phone_number=phone_number,password=password,email=email)
        db.add(new_user)
        db.commit()
        return True


def get_all_users_db():
    with next(get_db()) as db:
        all_users = db.query(User).all()
        return all_users


def get_exact_user_db(user_id):
    with next(get_db()) as db:
        exact_user=db.query(User).filter_by(id=user_id).first()
        if exact_user:
            return exact_user
        return False


def delete_exact_user(user_id):
    with next(get_db()) as db:
        ex_del_user = db.query(User).filter_by(id=user_id).first()
        if ex_del_user:
            db.delete(ex_del_user)
            db.commit()
            return True
        return False

def delete_all_user():
    with next(get_db()) as db:
        ex_del_user = db.query(User).all()
        if ex_del_user:
            for user in ex_del_user:
                db.delete(user)
            db.commit()
            return True
    return False



def update_user_db(user_id, change_info, new_info):
    with next(get_db()) as db:
        exact_user = db.query(User).filter_by(id=user_id).first()
        if exact_user:
            if change_info == "username":
                exact_user.username = new_info
            elif change_info == "email":
                exact_user.email = new_info
            elif change_info == "phone_number":
                exact_user.phone_number = new_info
            elif change_info == "password":
                exact_user.password = new_info
            db.commit()
            return True
        return False



