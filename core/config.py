
from datetime import timedelta

# Security / JWT
SECRET_KEY = "supersecretkey_change_this_in_prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # adjust as needed

# DB collection name (reused if needed)
COLLECTION_NAME = "employees"
