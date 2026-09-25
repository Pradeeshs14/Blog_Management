import os
import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.database import get_db
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth0 Authentication"],
)


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


@router.get("/login/")
def auth0_login(connection: str = "google-oauth2"):

    allowed_connections = {
        "google-oauth2",
        "facebook-custom",
    }

    if connection not in allowed_connections:
        raise HTTPException(
            status_code=400,
            detail="Invalid social login provider",
        )

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "connection": connection,
        "prompt": "consent",
    }

    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"{urlencode(params)}"
    )

    return RedirectResponse(url=auth_url)


@router.get("/login/google/")
def google_login():
    return auth0_login(connection="google-oauth2")


@router.get("/login/facebook/")
def facebook_login():
    return auth0_login(connection="facebook-custom")


@router.get("/callback/")
async def auth0_callback(
    request: Request,
    code: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    db: Session = Depends(get_db),
):

    if error:
        raise HTTPException(
            status_code=400,
            detail=error_description or error,
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing authorization code",
        )

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            token_url,
            data=payload,
        )

    if response.status_code != 200:
        print("AUTH0 TOKEN ERROR:", response.status_code)
        print("AUTH0 TOKEN RESPONSE:", response.text)

        raise HTTPException(
            status_code=400,
            detail="Failed to exchange authorization code with Auth0",
        )

    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Auth0 access token missing",
        )

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            f"https://{AUTH0_DOMAIN}/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        )

    if user_response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Failed to retrieve user information from Auth0",
        )

    user_info = user_response.json()

    print("AUTH0 USER INFO:", user_info)

    auth0_id = user_info.get("sub")
    email = user_info.get("email")
    name = user_info.get("name") or user_info.get("nickname")

    if not auth0_id:
        raise HTTPException(
            status_code=400,
            detail="Auth0 user ID missing",
        )

    if auth0_id.startswith("google-oauth2|"):
        provider = "google"

    elif auth0_id.startswith("facebook|"):
        provider = "facebook"

    else:
        provider = "facebook"

    user = (
        db.query(User)
        .filter(User.auth0_id == auth0_id)
        .first()
    )

    if not user and email:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    if user:

        user.name = name
        user.provider = provider
        user.auth0_id = auth0_id

    else:

        base_username = (
            user_info.get("nickname")
            or (email.split("@")[0] if email else None)
            or name
            or "user"
        )

        base_username = base_username[:45]

        username = base_username
        counter = 1

        while (
            db.query(User)
            .filter(User.username == username)
            .first()
        ):
            username = f"{base_username[:44]}{counter}"
            counter += 1

        user = User(
            username=username,
            email=email,
            password=hash_password(
                secrets.token_urlsafe(32)
            ),
            name=name,
            provider=provider,
            auth0_id=auth0_id,
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    local_jwt = create_access_token(user.id)

    request.session["access_token"] = local_jwt

    return RedirectResponse(
    url="/dashboard",
    status_code=302,
)

@router.get("/session/")
def get_auth_session(request: Request):

    access_token = request.session.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No active Auth0 session",
        )

    request.session.pop("access_token", None)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }