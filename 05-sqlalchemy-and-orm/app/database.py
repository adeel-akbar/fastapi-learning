import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("URL")
# engine is the gateway to the url we provided (our database)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(    #this is the session factory
    bind = engine,       #will define what each session will
    autoflush = False,    #have or provide us.
    autocommit = False
)

Base = declarative_base()

