#contract between the client and the server and validation

from pydantic import BaseModel, Field

#basic User for both student and teacher
class User(BaseModel):
    id: str =Field(..., min_length=9, max_length=9)#for chack that id with 9 digits
    full_name: str
    class_name: str

class Teacher(User):
    pass

class Student(User):
    pass

class DMS(BaseModel):
    Degrees: str=Field(..., min_length=1, max_length=2)
    Minutes: str=Field(..., min_length=1, max_length=2)
    Seconds: str=Field(..., min_length=1, max_length=2)

class Coordinates(BaseModel):
    Latitude: DMS
    Longitude: DMS
 
class Location(BaseModel):
    ID: str =Field(..., min_length=9, max_length=9)#for chack that id with 9 digits
    Coordinates: Coordinates
    Time: str= Field(..., pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
