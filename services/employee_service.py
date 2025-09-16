
from datetime import datetime, date
from typing import List, Optional, Dict, Any

from fastapi import HTTPException

from db.database import employees_collection
from models.employee_model import EmployeeCreate, EmployeeUpdate


# Helper to format joining_date for responses
def _format_joining_date(jd) -> Optional[str]:
    if jd is None:
        return None
    if isinstance(jd, datetime):
        return jd.date().isoformat()
    try:
        return jd.isoformat()
    except Exception:
        return str(jd)


def employee_helper(emp: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(emp.get("_id")),
        "employee_id": emp.get("employee_id"),
        "name": emp.get("name"),
        "department": emp.get("department"),
        "salary": emp.get("salary"),
        "joining_date": _format_joining_date(emp.get("joining_date")),
        "skills": emp.get("skills", []),
    }


# CREATE single employee
async def create_employee(payload: EmployeeCreate) -> Dict[str, Any]:
    last_emp = await employees_collection.find_one(
        {"employee_id": {"$regex": "^E\\d{3}$"}}, sort=[("employee_id", -1)]
    )
    if last_emp:
        try:
            last_id = int(last_emp["employee_id"][1:])
            new_emp_id = f"E{last_id + 1:03d}"
        except Exception:
            new_emp_id = "E001"
    else:
        new_emp_id = "E001"

    doc = payload.dict()
    doc["employee_id"] = new_emp_id

    # convert joining_date to datetime for Mongo if it's a date
    if isinstance(doc.get("joining_date"), date) and not isinstance(doc.get("joining_date"), datetime):
        doc["joining_date"] = datetime.combine(doc["joining_date"], datetime.min.time())

    result = await employees_collection.insert_one(doc)
    created = await employees_collection.find_one({"_id": result.inserted_id})
    return employee_helper(created)


# BULK CREATE
async def create_employees_bulk(payload: List[EmployeeCreate]) -> List[Dict[str, Any]]:
    last_emp = await employees_collection.find_one(
        {"employee_id": {"$regex": "^E\\d{3}$"}}, sort=[("employee_id", -1)]
    )
    start_id = int(last_emp["employee_id"][1:]) if last_emp else 0

    docs = []
    for i, emp in enumerate(payload, start=1):
        new_emp_id = f"E{start_id + i:03d}"
        doc = emp.dict()
        doc["employee_id"] = new_emp_id
        if isinstance(doc.get("joining_date"), date) and not isinstance(doc.get("joining_date"), datetime):
            doc["joining_date"] = datetime.combine(doc["joining_date"], datetime.min.time())
        docs.append(doc)

    if docs:
        result = await employees_collection.insert_many(docs)
        cursor = employees_collection.find({"_id": {"$in": result.inserted_ids}})
        created_emps = []
        async for doc in cursor:
            created_emps.append(employee_helper(doc))
        return created_emps
    return []


# GET by employee_id
async def get_employee(employee_id: str) -> Dict[str, Any]:
    emp = await employees_collection.find_one({"employee_id": employee_id})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_helper(emp)


# LIST employees with optional department filter + pagination
async def list_employees(department: Optional[str] = None, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
    q = {}
    if department:
        q["department"] = department

    cursor = employees_collection.find(q).sort("joining_date", -1).skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        results.append(employee_helper(doc))
    return results


# SEARCH by skill
async def search_by_skill(skill: str) -> List[Dict[str, Any]]:
    cursor = employees_collection.find({"skills": {"$in": [skill]}})
    results = []
    async for doc in cursor:
        results.append(employee_helper(doc))
    return results


# AVG salary by department (aggregation)
async def avg_salary_by_department() -> List[Dict[str, Any]]:
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": {"$round": ["$avg_salary", 2]}, "_id": 0}},
    ]
    cursor = employees_collection.aggregate(pipeline)
    out = []
    async for doc in cursor:
        out.append(doc)
    return out


# UPDATE partial
async def update_employee(employee_id: str, payload: EmployeeUpdate) -> Dict[str, Any]:
    update_data = payload.dict(exclude_unset=True)
    update_data.pop("employee_id", None)
    update_data.pop("_id", None)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    if "joining_date" in update_data and update_data["joining_date"] is not None:
        jd = update_data["joining_date"]
        if isinstance(jd, date) and not isinstance(jd, datetime):
            update_data["joining_date"] = datetime.combine(jd, datetime.min.time())

    result = await employees_collection.update_one({"employee_id": employee_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp = await employees_collection.find_one({"employee_id": employee_id})
    return employee_helper(emp)


# DELETE
async def delete_employee(employee_id: str) -> Dict[str, str]:
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": "Deleted successfully"}
