from pydantic import BaseModel
from typing import Optional


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
    status: Optional[str] = "1"


# ▶️ Used for reading student data (output)
class StudentOut(BaseModel):
    id: int
    studentName: str
    batchName: str
    contactNumber: str
    guardianNumber: Optional[str]
    initialPayment: float
    totalPayment: float
    noOfDues: int
    remarks: Optional[str]
    studentPhoto: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True  # ✅ or use orm_mode = True
