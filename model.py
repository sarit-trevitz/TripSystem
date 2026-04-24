#database table definitions
from sqlalchemy import Column, String
from sqlLiteDB import Base

#Teacher table
class Teacher(Base):
        __tablename__ = "teachers"
        id = Column(String, primary_key=True)
        full_name = Column(String)
        class_name = Column(String)

#Student table
class Student(Base):
        __tablename__ = "students"
        id = Column(String, primary_key=True)
        full_name = Column(String)
        class_name = Column(String)