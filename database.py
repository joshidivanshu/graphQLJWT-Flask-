from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

engine = create_engine('mysql://root:divanshu@localhost/jwt', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20),unique=True,nullable=False)
    password = Column(String(60),nullable=False)
    email = Column(String(100))
    stores = relationship('Store',backref='owner')
    
class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String(20),unique=True,nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'))

Base.metadata.create_all(engine)    