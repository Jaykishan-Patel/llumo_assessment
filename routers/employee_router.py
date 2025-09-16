# llumo/routers/employee_router.py
from fastapi import APIRouter, Depends, Query, Body
from typing import List, Optional

from core.auth import get_current_user
from models.employee_model import EmployeeCreate, EmployeeUpdate, AvgSalaryOut
from services.employee_service import (
    create_employee,
    create_employees_bulk,
    list_employees,
    get_employee,
    search_by_skill,
    avg_salary_by_department,
    update_employee,
    delete_employee,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", status_code=201, dependencies=[Depends(get_current_user)])
async def api_create_employee(payload: EmployeeCreate):
    return await create_employee(payload)


@router.post("/bulk", status_code=201, dependencies=[Depends(get_current_user)])
async def api_create_employees_bulk(payload: List[EmployeeCreate] = Body(...)):
    created = await create_employees_bulk(payload)
    return {"employees_added": created}


@router.get("", response_model=List[dict])
async def api_list_employees(department: Optional[str] = Query(None), skip: int = 0, limit: int = 50):
    return await list_employees(department=department, skip=skip, limit=limit)


@router.get("/search", response_model=List[dict])
async def api_search_by_skill(skill: str = Query(...)):
    return await search_by_skill(skill)


@router.get("/avg-salary", response_model=List[AvgSalaryOut])
async def api_avg_salary_by_department():
    return await avg_salary_by_department()


@router.get("/{employee_id}")
async def api_get_employee(employee_id: str):
    return await get_employee(employee_id)


@router.put("/{employee_id}", dependencies=[Depends(get_current_user)])
async def api_update_employee(employee_id: str, payload: EmployeeUpdate):
    return await update_employee(employee_id, payload)


@router.delete("/{employee_id}", dependencies=[Depends(get_current_user)])
async def api_delete_employee(employee_id: str):
    return await delete_employee(employee_id)
