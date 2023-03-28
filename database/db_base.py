from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy_utils import database_exists, create_database

engine = create_engine('mysql+pymysql://root:Password123@localhost:3333/pebble')
if not database_exists(engine.url):
    create_database(engine.url)
Session = sessionmaker(bind=engine)

DBBase = declarative_base()
