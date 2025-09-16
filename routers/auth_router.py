
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import login_for_access_token

router = APIRouter(tags=["auth"])


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Obtain JWT access token.
    Demo credentials: username=admin password=password
    """
    return await login_for_access_token(form_data)
