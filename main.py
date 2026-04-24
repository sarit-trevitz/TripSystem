#Main API routes and logic for the Trip System
from fastapi import FastAPI, Depends, HTTPException
import model
import schema
from sqlLiteDB import engine, SessionLocal
from sqlalchemy.orm import Session

#make the tables that defined in the models.py file in the database
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Root endpoint to check if the API is online and running successfully
@app.get("/")
def read_root_home():
    return {"message": "Trip System API is running!"}  

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
         raise HTTPException(status_code=400, detail="Teacher already exists")
        new_teacher = model.Teacher(id=teacher.id, full_name=teacher.full_name, class_name=teacher.class_name)
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        return {"message": "Teacher created successfully"}


#create a new student
@app.post("/students")
def create_student(student: schema.Student, db: Session = Depends(get_db)):
        if db.query(model.Student).filter_by(id=student.id).first():
         raise HTTPException(status_code=400, detail="Student already exists")
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
                "class_name": teacher.class_name
            }
            for teacher in teachers
        ],
        "students": [
            {
                "id": student.id,
                "full_name": student.full_name,
                "class_name": student.class_name
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

