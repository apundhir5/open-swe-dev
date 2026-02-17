"""
FastAPI web application with secure login flow.
"""
from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

from .security import authenticate_user, create_session_token, verify_session_token

# Initialize FastAPI app
app = FastAPI(title="Minimal Web App", description="A minimal web app with secure login flow")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Session cookie configuration
COOKIE_NAME = "session"
COOKIE_MAX_AGE = 3600  # 1 hour
COOKIE_HTTPONLY = True
COOKIE_SAMESITE = "lax"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: Optional[str] = Cookie(None)):
    """
    Home page route.
    
    If no valid session cookie → page says "You are not logged in."
    If logged in → page greets "Welcome, <username>."
    """
    username = None
    
    if session:
        username = verify_session_token(session)
    
    return templates.TemplateResponse(
        "home.html", 
        {"request": request, "username": username}
    )


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: Optional[int] = None):
    """
    Login form route.
    
    Renders a simple form: username, password, submit.
    If query param ?error=1 present, show "Invalid credentials."
    """
    show_error = error == 1
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": show_error}
    )


@app.post("/login")
async def login_submit(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Login form submission route.
    
    On valid creds: set signed session cookie; redirect (302) to /.
    On invalid creds: redirect (302) to /login?error=1.
    """
    user = authenticate_user(username, password)
    
    if user:
        # Valid credentials - create session token and set cookie
        session_token = create_session_token(username)
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key=COOKIE_NAME,
            value=session_token,
            max_age=COOKIE_MAX_AGE,
            httponly=COOKIE_HTTPONLY,
            samesite=COOKIE_SAMESITE
        )
        return response
    else:
        # Invalid credentials - redirect to login with error
        return RedirectResponse(url="/login?error=1", status_code=302)


@app.get("/logout")
async def logout():
    """
    Logout route.
    
    Clears cookie; redirect (302) to /.
    """
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key=COOKIE_NAME)
    return response


# Health check endpoint (useful for deployment)
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
