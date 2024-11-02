from db import get_db

from db.models import Worker_post,Worker


def register_worker_db(worker_name,phone_number,password,email):
    with next(get_db()) as db:
        new_user = Worker(worker_name=worker_name,phone_number=phone_number,password=password,email=email)
        db.add(new_user)
        db.commit()
        return True


def get_all_worker_db():
    with next(get_db()) as db:
        all_users = db.query(Worker).all()
        return all_users


def get_exact_worker_db(user_id):
    with next(get_db()) as db:
        exact_user=db.query(Worker).filter_by(id=user_id).first()
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



def chek_status(worker_id):
    with next(get_db()) as db:
        exact_worker=db.query(Worker_post).filter_by(id=worker_id).first()
        if exact_worker:
            if exact_worker.status == True:
                return True
            elif exact_worker.status == False:
                return 'Error'
        return False


def add_worker_post(worker_name:str,phone_number:str,main_text:str,status:bool):
    with next(get_db()) as db:
        new_post = Worker_post(worker_name=worker_name,
                               phone_number=phone_number,main_text=main_text,
                               status=status)
        db.add(new_post)
        db.commit()
        return True

def get_exact_worker_post_db(worker_id):
    with next(get_db()) as db:
        exact_user=db.query(Worker_post).filter_by(id=worker_id).first()
        if exact_user:
            return exact_user
        return False

def all_worker_post_db():
    with next(get_db()) as db:
        exact_user=db.query(Worker_post).all()
        if exact_user:
            return exact_user
        return False


def update_worker_post_db(worker_id, change_info, new_info):
    with next(get_db()) as db:
        exact_user = db.query(Worker_post).filter_by(id=worker_id).first()
        if exact_user:
            if change_info == "worker_name":
                exact_user.worker_name = new_info
            elif change_info == "phone_number":
                exact_user.phone_number = new_info
            elif change_info == "status":
                exact_user.status = new_info
                if new_info == True or False:
                    pass
            elif change_info == "main_text":
                exact_user.main_text = new_info

            try:
                db.commit()
                return True
            except Exception as e:
                db.rollback()  # Отменяем изменения в случае ошибки
                print(f"Error committing changes: {e}")
                return False




def delete_exact_worker_post_status(worker_post_id):
    with next(get_db()) as db:
        ex_del_user = db.query(Worker_post).filter_by(id=worker_post_id).first()
        if ex_del_user:
            for worker in ex_del_user:
                db.delete(worker)
            db.commit()
            return True
        return False


