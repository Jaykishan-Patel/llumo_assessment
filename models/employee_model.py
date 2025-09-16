from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class EmployeeCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    department: str = Field(..., example="Engineering")
    salary: float = Field(..., example=75000)
    joining_date: date = Field(..., example="2023-01-15")
    skills: List[str] = Field(default_factory=list, example=["Python", "MongoDB"])


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None


class AvgSalaryOut(BaseModel):
    department: str
    avg_salary: float
