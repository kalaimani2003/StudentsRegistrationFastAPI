from pydantic import BaseModel
from typing import Optional
from datetime import date

# ▶️ Used when creating a student
class StudentCreate(BaseModel):
    studentPhoto: Optional[str] = None
    studentName: str
    batchName: str
    contactNumber: str
    guardianNumber: Optional[str] = None
    initialPayment: float
    totalPayment: float
    noOfDues: int
    remarks: Optional[str] = None
    status: Optional[str] = 1

# ✅ Used for response (after saving student)
class StudentOut(StudentCreate):
    id: int

    class Config:
        orm_mode = True
