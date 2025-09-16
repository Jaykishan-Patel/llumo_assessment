

# Employees API (FastAPI + MongoDB)

A high-performance REST API to manage employees with CRUD, department-filtered listing by newest joining date, skills search, and average salary aggregation, aligned with the assessment brief.[1]
Security uses OAuth2 Password flow with Bearer JWT tokens for protected routes, following FastAPI’s recommended approach.[2][3]

## Features

- CRUD operations for employees with 404 on missing records and uniqueness on employee_id.[1]
- List employees by department sorted by newest joining_date via a query parameter.[1]
- Search employees by skill from the skills array and compute average salary per department.[1]
- JWT authentication for protected routes, pagination support, JSON schema validation, and unique indexes for integrity.[1]


## Running the API

Start the server using Uvicorn and open the interactive API docs at /docs after startup.[4]
- Development example: uvicorn main:app --reload[4]

```bash
uvicorn main:app --reload
```

## Authentication

- Obtain a token by POSTing OAuth2 Password form fields username and password to the token endpoint.[5][2]
- Send Authorization: Bearer <token> to access protected routes, as per FastAPI’s OAuth2PasswordBearer flow with JWT.[3][5]

## API endpoints

### 1) Create Employee (POST)
- Endpoint: /employees (Protected)[1]
- Inserts a new employee; ensure employee_id uniqueness per assessment requirements.[1]
- Request body example:[1]
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

### 2) Get Employee by ID (GET)
- Endpoint: /employees/{employee_id} (Public)[1]
- Returns employee details or 404 if not found.[1]
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

### 3) Update Employee (PUT)
- Endpoint: /employees/{employee_id} (Protected)[1]
- Partial updates are allowed; only provided fields are modified.[1]
```json
{
  "salary": 80000,
  "skills": ["Python", "FastAPI", "MongoDB"]
}
```

### 4) Delete Employee (DELETE)
- Endpoint: /employees/{employee_id} (Protected)[1]
- Deletes the employee and returns a success or failure message.[1]

### 5) List Employees by Department (GET)
- Endpoint: /employees (Public)[1]
- Query params: department (required for filtering), skip, limit; results sorted by joining_date desc.[1]
```http
GET /employees?department=Engineering&skip=0&limit=5
```

### 6) Average Salary per Department (GET)
- Endpoint: /employees/avg-salary (Public)[1]
- Returns average salaries grouped by department as an array of objects.[1]
```json
[
  { "department": "Engineering", "avg_salary": 80000 },
  { "department": "HR", "avg_salary": 60000 }
]
```

### 7) Search Employees by Skill (GET)
- Endpoint: /employees/search (Public)[1]
- Query param: skill; returns employees whose skills include the provided value.[1]
```http
GET /employees/search?skill=Python
```

## Sample document

This is the canonical shape of an employee document used across requests and responses.[1]
```json
{
  "employee_id": "E123",
  "name": "John Doe",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "MongoDB", "APIs"]
}

[19](https://betterstack.com/community/guides/scaling-python/authentication-fastapi/)
[20](https://app-generator.dev/docs/technologies/fastapi/security-best-practices.html)
[21](https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Advanced-FastAPI/Creating-A-Token)
