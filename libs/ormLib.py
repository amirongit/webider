from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class domain(Base):

    __tablename__ = 'domains'
    
    Id = Column('id', Integer, primary_key=True)
    url = Column('url', String, unique=True)

def create_data_base(path):
    
    engin = create_engine('sqlite:///' + path + 'webider.db')
    Base.metadate.create_all(bind=engin)

    session = sessionmaker()
    
    return session()
