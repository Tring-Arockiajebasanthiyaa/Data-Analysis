from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import psycopg2
database_url="postgresql://postgres:sandy@localhost:5432/postgres"
engine=create_engine(database_url)
session = Session(engine)
print("Database connected")

##Create Table

base=declarative_base()

class User(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,index=True)
    email=Column(String,index=True)

base.metadata.create_all(bind=engine)
print("Table created")
    
