from sqlalchemy import Column, Integer, String, Date , Float
from app.database.connection import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    studentPhoto = Column(String(255), nullable=True)
    studentName = Column(String(100), nullable=False)
    batchName = Column(String(100), nullable=False)
    contactNumber = Column(String(20), nullable=False)
    guardianNumber = Column(String(20), nullable=True)
    initialPayment = Column(Float, nullable=False)
    totalPayment = Column(Float, nullable=False)
    noOfDues = Column(Integer, nullable=False)
    remarks = Column(String(255), nullable=True)
    status = Column(String(20), default=1)
