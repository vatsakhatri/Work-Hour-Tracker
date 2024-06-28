from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url=""
engine=create_engine(url)

local_session=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()