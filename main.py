
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo.errors import CollectionInvalid

from db.database import db, employees_collection
from routers.employee_router import router as employee_router
from routers.auth_router import router as auth_router
from core.config import COLLECTION_NAME

app = FastAPI(title="Employees API (MVVM structure)")

app.include_router(auth_router)
app.include_router(employee_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create unique index on employee_id and apply JSON Schema validation
    on startup. If collection already exists, attempt to collMod it.
    """
    print("Startup: ensure index and JSON schema")

    # Ensure unique index
    await employees_collection.create_index("employee_id", unique=True)

    # JSON Schema validator
    employee_schema = {
        "bsonType": "object",
        "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
        "properties": {
            "employee_id": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "department": {"bsonType": "string"},
            "salary": {"bsonType": ["double", "int"]},  # allow int/double
            "joining_date": {"bsonType": "date"},
            "skills": {"bsonType": "array", "items": {"bsonType": "string"}},
        },
    }

    try:
        # If collection doesn't exist, create with validator
        await db.create_collection(
            COLLECTION_NAME,
            validator={"$jsonSchema": employee_schema}
        )
        print("Created collection with JSON schema validator.")
    except Exception as exc:
        # If it exists, modify validator
        try:
            await db.command("collMod", COLLECTION_NAME, validator={"$jsonSchema": employee_schema})
            print("Applied JSON schema validator to existing collection.")
        except Exception as exc2:
            # Some Mongo versions / permissions might raise; continue but warn
            print("Warning: could not apply JSON schema validator:", exc2)

    yield
    print("Shutdown.")


# attach lifespan
app.router.lifespan_context = lifespan  # fastapi >=0.95 style; works with contextmanager above
# If the above binding doesn't work on older FastAPI versions, you can create app with lifespan param:
# app = FastAPI(title="Employees API (MVVM structure)", lifespan=lifespan)

# Root health-check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Employees API running"}
