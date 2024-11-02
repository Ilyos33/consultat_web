from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey,BigInteger
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class User(Base):
    __tablename__='users'

    id=Column(Integer, autoincrement=True, primary_key=True)
    user_name=Column(String(55), nullable=False,unique=True)
    phone_number = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    reg_data = Column(DateTime, default=datetime.now())

class Worker(Base):
    __tablename__='worker'
    id=Column(Integer, autoincrement=True, primary_key=True)
    worker_name = Column(String,nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    reg_data = Column(DateTime,default=datetime.now())


class Worker_post(Base):
    __tablename__='workerpost'

    id=Column(Integer, autoincrement=True, primary_key=True)
    worker_name = Column(String,ForeignKey("worker.worker_name"))
    phone_number = Column(String,ForeignKey("worker.phone_number"))
    main_text = Column(String)
    status = Column(Boolean,default=True)
    reg_data = Column(DateTime, default=datetime.now())

    user_fk_phone =relationship(Worker,lazy='subquery', foreign_keys=[phone_number])
    user_fk_name =relationship(Worker,lazy='subquery', foreign_keys=[worker_name])






