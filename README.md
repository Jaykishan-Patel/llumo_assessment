

## Features

- **CRUD** operations for employees
- **List employees by department** sorted by newest joining date
- **Search employees by skills**
- **Calculate average salary per department**
- **JWT authentication** for protected routes
- **Pagination support** for listings
- **MongoDB JSON schema validation** and **unique indexes** for data integrity

---

## Requirements

- Python 3.10+
- MongoDB (local)
- Dependencies in `requirements.txt`:
  - `fastapi`
  - `uvicorn`
  - `motor`
  - `pydantic`
  - `python-jose`
  - `passlib`
  - `pymongo`
  - `python-multipart`

---

## Setup

1. **Clone the repository** or download the project.

2. **Create and activate a virtual environment:**

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
````

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Ensure MongoDB is running locally** and accessible via `MONGO_URL`.

---

## Environment Variables

Create a `.env` file in the project root with:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=assessment_db
COLLECTION_NAME=employees

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Running the API

Start the server:

```bash
uvicorn main:app --reload
```

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Authentication

* Obtain a JWT token by POSTing `username` and `password` to:

```
POST /token
```

* Use the token in the `Authorization` header for protected routes:

```
Authorization: Bearer <token>
```

> Create, update, and delete routes are protected.

---

## API Endpoints

### 1. Create Employee (POST)

**Endpoint:** `/employees`
**Protected:** Yes

**Request Body:**

```json
{
  "employee_id": "E123",
  "name": "John Doe",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "MongoDB", "APIs"]
}
```

**Response Example:**

```json
{
  "message": "Employee created successfully",
  "employee_id": "E123"
}
```

---

### 2. Get Employee by ID (GET)

**Endpoint:** `/employees/{employee_id}`
**Protected:** No

**Response Example:**

```json
{
  "employee_id": "E123",
  "name": "John Doe",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "MongoDB", "APIs"]
}
```

**404 Example:**

```json
{
  "detail": "Employee not found"
}
```

---

### 3. Update Employee (PUT)

**Endpoint:** `/employees/{employee_id}`
**Protected:** Yes

**Request Body:** *(partial fields allowed)*

```json
{
  "salary": 80000,
  "skills": ["Python", "FastAPI", "MongoDB"]
}
```

**Response Example:**

```json
{
  "message": "Employee updated successfully",
  "employee_id": "E123"
}
```

---

### 4. Delete Employee (DELETE)

**Endpoint:** `/employees/{employee_id}`
**Protected:** Yes

**Response Example:**

```json
{
  "message": "Employee deleted successfully",
  "employee_id": "E123"
}
```

**404 Example:**

```json
{
  "detail": "Employee not found"
}
```

---

### 5. List Employees by Department (GET)

**Endpoint:** `/employees`
**Query Parameters:**

* `department` (required)
* `skip` (optional, default 0)
* `limit` (optional, default 10)

**Example:** `/employees?department=Engineering&skip=0&limit=5`

**Response Example:**

```json
[
  {
    "employee_id": "E124",
    "name": "Jane Smith",
    "department": "Engineering",
    "salary": 85000,
    "joining_date": "2023-02-10",
    "skills": ["Python", "APIs"]
  },
  {
    "employee_id": "E123",
    "name": "John Doe",
    "department": "Engineering",
    "salary": 75000,
    "joining_date": "2023-01-15",
    "skills": ["Python", "MongoDB", "APIs"]
  }
]
```

---

### 6. Average Salary per Department (GET)

**Endpoint:** `/employees/avg-salary`
**Protected:** No

**Response Example:**

```json
[
  {
    "department": "Engineering",
    "average_salary": 80000
  },
  {
    "department": "HR",
    "average_salary": 60000
  }
]
```

---

### 7. Search Employees by Skill (GET)

**Endpoint:** `/employees/search`
**Query Parameter:** `skill` (required)

**Example:** `/employees/search?skill=Python`

**Response Example:**

```json
[
  {
    "employee_id": "E123",
    "name": "John Doe",
    "department": "Engineering",
    "salary": 75000,
    "joining_date": "2023-01-15",
    "skills": ["Python", "MongoDB", "APIs"]
  },
  {
    "employee_id": "E124",
    "name": "Jane Smith",
    "department": "Engineering",
    "salary": 85000,
    "joining_date": "2023-02-10",
    "skills": ["Python", "APIs"]
  }
]
```

---

## Sample Employee Document

```json
{
  "employee_id": "E123",
  "name": "John Doe",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "MongoDB", "APIs"]
}
```

---

