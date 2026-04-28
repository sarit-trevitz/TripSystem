#database table definitions
from sqlalchemy import Column, Float, ForeignKey, Integer, String
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

#Location table
class Location(Base):
        __tablename__ = "locations"
        id = Column(Integer, primary_key=True,index=True)
        student_id = Column(String, ForeignKey("students.id"))
        latitude = Column(Float)
        longitude = Column(Float) 
        time=Column(String)  