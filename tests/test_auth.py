"""
Comprehensive test suite for authentication functionality.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_home_anon():
    """
    Test that GET / returns 200 and contains "You are not logged in" for anonymous users.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        
        assert response.status_code == 200
        assert "You are not logged in" in response.text


@pytest.mark.asyncio
async def test_login_success_sets_cookie_and_redirects():
    """
    Test that POST /login with admin/admin123 returns 302, 
    response has set-cookie, and location header points to /.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=False
        )
        
        assert response.status_code == 302
        assert response.headers["location"] == "/"
        
        # Check that session cookie is set
        cookies = response.cookies
        assert "session" in cookies
        assert cookies["session"] is not None


@pytest.mark.asyncio
async def test_login_failure_redirects_with_error():
    """
    Test that POST /login with wrong password returns 302 to /login?error=1.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/login",
            data={"username": "admin", "password": "wrongpassword"},
            follow_redirects=False
        )
        
        assert response.status_code == 302
        assert response.headers["location"] == "/login?error=1"


@pytest.mark.asyncio
async def test_home_logged_in_shows_username():
    """
    Test that after successful login, follow-up GET / with returned cookie 
    contains 'Welcome, <strong>admin</strong>' (or equivalent clear greeting with "admin").
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # First, perform login to get session cookie
        login_response = await client.post(
            "/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=False
        )
        
        assert login_response.status_code == 302
        session_cookie = login_response.cookies.get("session")
        assert session_cookie is not None
        
        # Now make request to home page with the session cookie
        home_response = await client.get(
            "/",
            cookies={"session": session_cookie}
        )
        
        assert home_response.status_code == 200
        # Check for the specific greeting format with strong tag
        assert "Welcome, <strong>admin</strong>" in home_response.text


@pytest.mark.asyncio
async def test_login_form_shows_error():
    """
    Additional test to verify login form shows error message when error=1 parameter is present.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/login?error=1")
        
        assert response.status_code == 200
        assert "Invalid credentials" in response.text


@pytest.mark.asyncio
async def test_logout_clears_cookie():
    """
    Additional test to verify logout functionality clears the session cookie.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # First login to get a session
        login_response = await client.post(
            "/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=False
        )
        
        session_cookie = login_response.cookies.get("session")
        assert session_cookie is not None
        
        # Now logout
        logout_response = await client.get(
            "/logout",
            cookies={"session": session_cookie},
            follow_redirects=False
        )
        
        assert logout_response.status_code == 302
        assert logout_response.headers["location"] == "/"
        
        # Verify that the session cookie is cleared (deleted)
        # When a cookie is deleted, it's set with an empty value or expires in the past
        set_cookie_header = logout_response.headers.get("set-cookie", "")
        assert "session=" in set_cookie_header


@pytest.mark.asyncio
async def test_health_endpoint():
    """
    Additional test for the health check endpoint.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}







