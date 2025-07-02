from sqlalchemy.orm import Session
from app.models.student_model import Student
from app.schemas.student_schema import StudentCreate

# ▶️ Create student
def create_student(db: Session, student: StudentCreate):
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 📥 Get all students
def get_all_students(db: Session):
    return db.query(Student).all()
