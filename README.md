# Minimal Python Web App with Secure Login Flow

A tiny web application demonstrating secure authentication with FastAPI, Jinja2 templates, and session-based login. Features HTML login forms, bcrypt password hashing, signed cookies, comprehensive tests, and automated CI/CD deployment to Azure App Service.

## ⚡ Quick Start

### Prerequisites
- Python 3.11 or higher
- Git

### Setup and Run Locally

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 3000
   ```

5. **Access the application**
   - Open your browser and go to: http://localhost:3000
   - You should see the home page with login options

## 🔐 Demo Credentials

**⚠️ WARNING: These are demo credentials for development only. DO NOT use in production!**

- **Username**: `admin`
- **Password**: `admin123`

## 🧪 Testing

Run the test suite to verify everything works correctly:

```bash
pytest -q
```

### Test Coverage
The test suite includes:
- Anonymous user home page access
- Successful login with cookie setting
- Failed login with error handling
- Authenticated user home page access
- Login form error display
- Logout functionality
- Health check endpoint

## 🚀 Azure Deployment

### Step 1: Create Azure Web App

1. Log in to the [Azure Portal](https://portal.azure.com)
2. Create a new **Web App** resource
3. Choose **Python 3.11** as the runtime stack
4. Note down your **App Name** (e.g., `my-webapp-name`)

### Step 2: Get Publish Profile

1. In your Azure Web App, go to **Overview**
2. Click **Get publish profile** and download the `.publishsettings` file
3. Open the file and copy its entire contents

### Step 3: Configure GitHub Secrets

In your GitHub repository, go to **Settings** → **Secrets and variables** → **Actions** and add:

1. **`AZURE_WEBAPP_NAME`**
   - Value: Your Azure Web App name (e.g., `my-webapp-name`)

2. **`AZURE_WEBAPP_PUBLISH_PROFILE`**
   - Value: The entire contents of your `.publishsettings` file

3. **`APP_SECRET`** (Optional but recommended)
   - Value: A secure random string for cookie signing
   - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### Step 4: Set APP_SECRET in Azure

1. In your Azure Web App, go to **Configuration**
2. Under **Application settings**, click **New application setting**
3. Add:
   - **Name**: `APP_SECRET`
   - **Value**: Same secure random string from Step 3
4. Click **Save**

### Step 5: Deploy

1. **Move workflow files** (required step):
   ```bash
   mkdir -p .github/workflows
   cp tmp-workflows/ci.yml .github/workflows/
   cp tmp-workflows/deploy.yml .github/workflows/
   ```

2. **Push to main branch**:
   ```bash
   git add .
   git commit -m "Add GitHub Actions workflows"
   git push origin main
   ```

3. The deployment will automatically trigger. Check the **Actions** tab in GitHub to monitor progress.

### Manual Deployment

You can also trigger deployment manually:
1. Go to **Actions** tab in GitHub
2. Select **Deploy to Azure** workflow
3. Click **Run workflow**

## 🛠️ Basic Troubleshooting

### Port Conflicts
If port 3000 is already in use:
```bash
# Try a different port
uvicorn app.main:app --reload --port 8000

# Or find and kill the process using port 3000
# On Windows
netstat -ano | findstr :3000
taskkill /PID <process_id> /F

# On macOS/Linux
lsof -ti:3000 | xargs kill -9
```

### Python Version Issues
Ensure you're using Python 3.11 or higher:
```bash
python --version
# Should show Python 3.11.x or higher

# If not, try
python3 --version
python3.11 --version
```

### Dependency Installation Issues
If pip install fails:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing with verbose output
pip install -r requirements.txt -v

# On some systems, you might need
python3 -m pip install -r requirements.txt
```

### Template Not Found Errors
If you get template errors, ensure you're running from the project root directory:
```bash
# Make sure you're in the correct directory
ls -la
# You should see: app/, tests/, requirements.txt, README.md

# Run from project root
uvicorn app.main:app --reload --port 3000
```

### Session/Cookie Issues
If login doesn't work:
1. Clear your browser cookies for localhost
2. Check that `APP_SECRET` is set (defaults to dev value if not)
3. Verify the application is running on the correct port

### Azure Deployment Issues

**Deployment fails with "secrets not found":**
- Ensure both `AZURE_WEBAPP_NAME` and `AZURE_WEBAPP_PUBLISH_PROFILE` secrets are set
- Check that secret names match exactly (case-sensitive)

**App doesn't start in Azure:**
- Verify `APP_SECRET` is set in Azure App Service Configuration
- Check Azure App Service logs for startup errors
- Ensure Python 3.11 runtime is selected

**502 Bad Gateway errors:**
- Check that the startup command is correct in Azure
- Verify all dependencies are properly installed
- Review Azure App Service logs

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── security.py          # Authentication & session management
│   └── templates/
│       ├── base.html        # Base template
│       ├── home.html        # Home page
│       └── login.html       # Login form
├── tests/
│   ├── __init__.py
│   └── test_auth.py         # Comprehensive test suite
├── .github/workflows/       # (after moving from tmp-workflows/)
│   ├── ci.yml              # Continuous Integration
│   └── deploy.yml          # Azure deployment
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

- **`APP_SECRET`**: Secret key for signing session cookies
  - Default: `"dev-secret-change-in-production"` (development only)
  - Production: Set to a secure random string

### Session Configuration

- **Cookie Name**: `session`
- **Max Age**: 3600 seconds (1 hour)
- **HTTP Only**: `true`
- **Same Site**: `lax`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest -q`
5. Submit a pull request

## 📄 License

This project is for demonstration purposes. Use at your own risk in production environments.
