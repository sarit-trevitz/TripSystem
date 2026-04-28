#Main API routes and logic for the Trip System
import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
import model
import schema
from sqlLiteDB import engine, SessionLocal
from sqlalchemy.orm import Session

#make the tables that defined in the models.py file in the database
model.Base.metadata.create_all(bind=engine)

app = FastAPI()
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# Root endpoint to check if the API is online and running successfully
@app.get("/")
def read_root_home():
    return FileResponse(os.path.join(frontend_path, "index.html"))
    #return {"message": "Trip System API is running!"}  

# Helper function for managing the database connection: opens a connection and closes it when the operation is complete
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create a new teacher
@app.post("/teachers")
def create_teacher(teacher: schema.Teacher, db: Session = Depends(get_db)):
        if db.query(model.Teacher).filter_by(id=teacher.id).first():
         raise HTTPException(status_code=400, detail="This ID belong to a teacher who already exists")
        if db.query(model.Student).filter_by(id=teacher.id).first():
         raise HTTPException(status_code=400, detail="This ID belong to a student so it cannot be used for a teacher")
        new_teacher = model.Teacher(id=teacher.id, full_name=teacher.full_name, class_name=teacher.class_name)
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        return {"message": "Teacher created successfully"}


#create a new student
@app.post("/students")
def create_student(student: schema.Student, db: Session = Depends(get_db)):
        if db.query(model.Student).filter_by(id=student.id).first():
         raise HTTPException(status_code=400, detail="This ID belong to a student who already exists")
        if db.query(model.Teacher).filter_by(id=student.id).first():
         raise HTTPException(status_code=400, detail="This ID belong to a teacher so it cannot be used for a student")
        new_student = model.Student(id=student.id, full_name=student.full_name, class_name=student.class_name)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"message": "Student created successfully"}


#get all teachers
@app.get("/teachers")
def get_all_teachers(db: Session = Depends(get_db)):
    teachers=db.query(model.Teacher).all()
    return [
        {
            "id": teacher.id,
            "full_name": teacher.full_name,
            "class_name": teacher.class_name
        }
        for teacher in teachers
    ]


#get all students
@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    students=db.query(model.Student).all()
    return [
        {
            "id": student.id,
            "full_name": student.full_name,
            "class_name": student.class_name
        }
        for student in students
    ]

#get a teacher by id
@app.get("/teachers/{teacher_id}")
def get_teacher_by_id(teacher_id: str, db: Session = Depends(get_db)):
    teacher = db.query(model.Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {
        "id": teacher.id,
        "full_name": teacher.full_name,
        "class_name": teacher.class_name
    }

#get a student by id
@app.get("/students/{student_id}")
def get_student_by_id(student_id: str, db: Session = Depends(get_db)):
    student = db.query(model.Student).filter_by(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "id": student.id,
        "full_name": student.full_name,
        "class_name": student.class_name
    }

#get all user-students and teachers
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):   
    teachers = db.query(model.Teacher).all()
    students = db.query(model.Student).all()
    return {
        "teachers": [
            {
                "id": teacher.id,
                "full_name": teacher.full_name,
                "class_name": teacher.class_name,
                "role": "teacher"
            }
            for teacher in teachers
        ],
        "students": [
            {
                "id": student.id,
                "full_name": student.full_name,
                "class_name": student.class_name,
                "role": "student"
            }
            for student in students
        ]
    }


#get all students in a specific class the teacher is teaching
@app.get("/teachers/{teacher_id}/students")
def get_students_in_class(teacher_id: str, db: Session = Depends(get_db)):
    teacher = db.query(model.Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    students_in_class = db.query(model.Student).filter_by(class_name=teacher.class_name).all()
    return [
        {
            "id": student.id,
            "full_name": student.full_name,
            "class_name": student.class_name
        }
        for student in students_in_class
    ]

#A function to send the right data to the frontend based on the type of table requested by the teacher user
@app.get("/get_table_data")
def get_table_data(type: str, teacher_id: str = None, db: Session = Depends(get_db)):
    if type == "all_teachers":
        return get_all_teachers(db)
    
    elif type == "all_students":
        return get_all_students(db)
    
    elif type == "all_users":
        data = get_all_users(db)
        return data["teachers"] + data["students"]

    elif type == "my_students":
        if not teacher_id:
            raise HTTPException(status_code=400, detail="Teacher ID is required")
        return get_students_in_class(teacher_id, db)
    
    raise HTTPException(status_code=400, detail="Invalid table type")

#stage 2
#helper function to convert DMS to decimal degrees
def dms_to_decimal(dms:schema.DMS):
    degree = float(dms.Degrees)
    minutes = float(dms.Minutes)
    seconds = float(dms.Seconds)
    if minutes>=60 or seconds>=60:
        raise HTTPException(status_code=400, detail="Minutes and seconds must be less than 60")
    return degree + (minutes / 60) + (seconds / 3600)

#receive location 
@app.post("/locations")
def receive_location(data: schema.Location, db: Session = Depends(get_db)):
    student = db.query(model.Student).filter_by(id=data.ID).first()
    teacher = None
    if not student:
       teacher = db.query(model.Teacher).filter_by(id=data.ID).first()
    if not student and not teacher:
        raise HTTPException(status_code=404, detail=f"Student or teacher with ID {data.ID} not found, so the location didn't save")
    try:
        lati = dms_to_decimal(data.Coordinates.Latitude)
        longi = dms_to_decimal(data.Coordinates.Longitude)
        new_location = model.Location(student_id=data.ID, latitude=lati, longitude=longi, time=data.Time)
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return {"message": "Location received successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid DMS format for latitude or longitude")   




 #get the latest location of a student by id
@app.get("/latest_locations")
def get_latest_locations(teacher_id: str = None, db: Session = Depends(get_db)):
    # find the latest location for each student 
    subquery = db.query(
        model.Location.student_id,
        func.max(model.Location.time).label('max_time')
    ).group_by(model.Location.student_id).subquery()

    # 2.find the location details for the latest location of each student
    query = db.query(model.Location).join(
        subquery, 
        (model.Location.student_id == subquery.c.student_id) & 
        (model.Location.time == subquery.c.max_time)
     ).join(model.Student, model.Location.student_id == model.Student.id)

    # 3. find just the students that the teacher is teaching if teacher_id is provided
    if teacher_id:
        teacher = db.query(model.Teacher).filter(model.Teacher.id == teacher_id).first()
        if teacher:
            query = query.filter(model.Student.class_name == teacher.class_name)

    results = query.all()
    # make a dictionary of the latest locations to ensure we only return one location per student.
    unique_locations = {}
    for loc in results:
        unique_locations[loc.student_id] = {
            "student_id": loc.student_id,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "time": loc.time
        }
    final_locations = list(unique_locations.values())    
    if teacher_id:
       
        teacher_loc = db.query(model.Location).filter(
            model.Location.student_id == teacher_id).order_by(model.Location.time.desc()).first()

        if teacher_loc:
            teacher_data = {
                "student_id": teacher_id,
                "latitude": teacher_loc.latitude,
                "longitude": teacher_loc.longitude,
                "time": teacher_loc.time
            }
            final_locations.insert(0, teacher_data)
          

    return final_locations

