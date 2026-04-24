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

    
