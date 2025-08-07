#!/usr/bin/env python3
"""
Simple verification script to test the application components.
"""

def verify_imports():
    """Verify all modules can be imported successfully."""
    try:
        from app.main import app
        from app.security import authenticate_user, create_session_token, verify_session_token
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def verify_security():
    """Verify security functions work correctly."""
    try:
        from app.security import authenticate_user, create_session_token, verify_session_token
        
        # Test authentication
        user = authenticate_user("admin", "admin123")
        if not user:
            print("❌ Authentication failed for valid credentials")
            return False
        
        # Test invalid authentication
        invalid_user = authenticate_user("admin", "wrongpassword")
        if invalid_user:
            print("❌ Authentication succeeded for invalid credentials")
            return False
        
        # Test token creation and verification
        token = create_session_token("admin")
        username = verify_session_token(token)
        if username != "admin":
            print("❌ Token verification failed")
            return False
        
        print("✅ Security functions working correctly")
        return True
    except Exception as e:
        print(f"❌ Security error: {e}")
        return False

def verify_app_routes():
    """Verify FastAPI app has all required routes."""
    try:
        from app.main import app
        
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                for method in route.methods:
                    routes.append(f"{method} {route.path}")
            elif hasattr(route, 'path'):
                routes.append(f"* {route.path}")
        
        required_routes = [
            "GET /",
            "GET /login", 
            "POST /login",
            "GET /logout",
            "GET /health"
        ]
        
        missing_routes = []
        for required in required_routes:
            if not any(required in route for route in routes):
                missing_routes.append(required)
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        
        print("✅ All required routes present")
        print("Available routes:")
        for route in sorted(routes):
            print(f"  {route}")
        return True
    except Exception as e:
        print(f"❌ Route verification error: {e}")
        return False

def main():
    """Run all verification checks."""
    print("🔍 Verifying Minimal Web App Components...")
    print("=" * 50)
    
    checks = [
        ("Module Imports", verify_imports),
        ("Security Functions", verify_security),
        ("App Routes", verify_app_routes)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All verification checks passed!")
        print("✅ Application is ready for local testing with uvicorn")
        print("\nTo start the application:")
        print("  uvicorn app.main:app --reload --port 3000")
    else:
        print("❌ Some verification checks failed")
        return False
    
    return True

if __name__ == "__main__":
    main()
