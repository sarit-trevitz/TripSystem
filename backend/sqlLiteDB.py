# The connection to the SQLLite database ans session configuration
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#create the database connection string for SQLAlchemy (the '.' mean the current directory) 
DATABASE_URL = "sqlite:///./trip_sys.db"

#create the SQLAlchemy engine for connecting to the SQLite database
engine=create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# create a sessionmaker factory for creating database sessions(The one who active the connection to the database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class for declarative models(Teacher and Student class will inherit from this base class)
Base = declarative_base()