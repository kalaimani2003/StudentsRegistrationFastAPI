import os
import shutil
import base64
import re
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.schemas.student_schema import StudentCreate, StudentOut
from app.crud.student_crud import create_student
from app.database.connection import get_db
from typing import List, Optional
from app.models.student_model import Student



router = APIRouter(
    prefix="/master",
    tags=["Students"]
)

UPLOAD_FOLDER = "assets/studentsphotos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/studentRegister", response_model=StudentOut)
async def register_student(
    studentName: str = Form(...),
    batchName: str = Form(...),
    contactNumber: str = Form(...),
    guardianNumber: str = Form(None),
    initialPayment: float = Form(...),
    totalPayment: float = Form(...),
    noOfDues: int = Form(...),
    remarks: str = Form(None),
    studentPhoto: UploadFile = File(None),
    studentPhotoBase64: str = Form(None),
    db: Session = Depends(get_db),
):
    photo_path = None

    # First save student without photo to get ID
    student_data = StudentCreate(
        studentPhoto=None,
        studentName=studentName,
        batchName=batchName,
        contactNumber=contactNumber,
        guardianNumber=guardianNumber,
        initialPayment=initialPayment,
        totalPayment=totalPayment,
        noOfDues=noOfDues,
        remarks=remarks
    )
    student = create_student(db, student_data)  # returns object with ID

    # Clean the student name for filename
    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', studentName)
    phone_suffix = contactNumber[-2:]
    ext = ".jpg"

    # Handle file upload
    if studentPhoto:
        ext = os.path.splitext(studentPhoto.filename)[1] or ".jpg"
        filename = f"{clean_name}_{student.id}_{phone_suffix}{ext}"
        file_location = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(studentPhoto.file, buffer)
        photo_path = f"/assets/studentsphotos/{filename}"
        # print(photo_path)


    # Handle base64 upload
    elif studentPhotoBase64:
        try:
            header, encoded = studentPhotoBase64.split(",", 1) if "," in studentPhotoBase64 else ("", studentPhotoBase64)
            data = base64.b64decode(encoded)
            filename = f"{clean_name}_{student.id}_{phone_suffix}.jpg"
            file_location = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_location, "wb") as f:
                f.write(data)
            photo_path = f"/assets/studentsphotos/{filename}"
            # print(photo_path)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 image: {str(e)}")

    # Update student record with photo path
    if photo_path:
        student.studentPhoto = photo_path
        db.commit()
        db.refresh(student)

    return student


# @router.get("/getStudents", response_model=List[StudentOut])
# def get_students(id: Optional[int] = None, db: Session = Depends(get_db)):
#     if id:
#         student = db.query(Student).filter(Student.id == id).all()
#         return student
#     return db.query(Student).all()

@router.get("/getStudents")
def get_students(id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(
        Student.id,
        Student.studentPhoto,
        Student.studentName,
        Student.batchName,
        Student.contactNumber,
        Student.totalPayment,
        Student.guardianNumber,
        Student.initialPayment,
        Student.noOfDues,
        Student.remarks,
        # Student.status
    )

    if id:
        query = query.filter(Student.id == id)

    results = query.all()

    students = []
    for row in results:
        students.append({
            "id": row.id,
            "studentPhoto": row.studentPhoto,
            "studentName": row.studentName,
            "batchName": row.batchName,
            "contactNumber": row.contactNumber,
            "totalPayment": row.totalPayment,
            "guardianNumber": row.guardianNumber,
            "initialPayment": row.initialPayment,
            "noOfDues": row.noOfDues,
            "remarks": row.remarks,
            # "status": row.status,
        })

    return students

@router.put("/updateStudent/{student_id}", response_model=StudentOut)
async def update_student(
    student_id: int,
    studentName: str = Form(...),
    batchName: str = Form(...),
    contactNumber: str = Form(...),
    guardianNumber: Optional[str] = Form(None),
    initialPayment: float = Form(...),
    totalPayment: float = Form(...),
    noOfDues: int = Form(...),
    remarks: Optional[str] = Form(None),
    studentPhoto: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', studentName)
    phone_suffix = contactNumber[-2:] if len(contactNumber) >= 2 else "00"

    new_photo_path = student.studentPhoto

    if studentPhoto:
        ext = os.path.splitext(studentPhoto.filename)[1] or ".jpg"
        filename = f"{clean_name}_{student.id}_{phone_suffix}{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Delete old photo if exists
        if student.studentPhoto:
            old_filename = student.studentPhoto.replace("/assets/studentsphotos/", "")
            old_file_path = os.path.join(UPLOAD_FOLDER, old_filename)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(studentPhoto.file, buffer)

        new_photo_path = f"/assets/studentsphotos/{filename}"

    # Update student fields
    student.studentName = studentName
    student.batchName = batchName
    student.contactNumber = contactNumber
    student.guardianNumber = guardianNumber
    student.initialPayment = initialPayment
    student.totalPayment = totalPayment
    student.noOfDues = noOfDues
    student.remarks = remarks
    student.studentPhoto = new_photo_path

    print("Received student ID:", student_id)
    print("Student Name:", studentName)
    print("File:", studentPhoto.filename if studentPhoto else "No new photo")


    db.commit()
    db.refresh(student)

    return student


@router.delete("/deleteStudent/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Delete photo from file system
    if student.studentPhoto:
        photo_path = student.studentPhoto.lstrip("/")  # remove leading slash
        if os.path.exists(photo_path):
            os.remove(photo_path)

    db.delete(student)
    db.commit()

    return {"message": f"Student with ID {student_id} deleted successfully"}

