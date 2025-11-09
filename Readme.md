
```markdown
# 📝 Task Manager API

> A full-featured RESTful API for task management with JWT authentication, MongoDB storage, and interactive Swagger documentation.

## 📖 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 About

Task Manager API is a production-ready backend service that enables users to manage their tasks efficiently. Built with Flask and MongoDB, it provides secure authentication, role-based access control, and a comprehensive REST API for task operations[web:31][web:35][web:36].

### What Problem Does It Solve?

- Provides secure task management with user isolation
- Offers JWT-based authentication for stateless API access
- Enables pagination and filtering for efficient data retrieval
- Includes comprehensive API documentation via Swagger UI

## ✨ Features

- 🔐 **JWT Authentication** - Secure token-based authentication system
- 👥 **User Management** - User registration, login, and role-based access
- ✅ **CRUD Operations** - Complete task management (Create, Read, Update, Delete)
- 📄 **Pagination** - Efficient data retrieval with customizable page sizes
- 🔍 **Filtering** - Filter tasks by completion status
- 📚 **Swagger Documentation** - Interactive API documentation at `/docs`
- 🧪 **Test Suite** - Comprehensive tests with 95%+ code coverage
- 🔒 **Security** - Password hashing with bcrypt, JWT token expiration
- 🗄️ **MongoDB** - Scalable NoSQL database with indexing
- 🌐 **CORS Support** - Cross-origin resource sharing enabled

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Flask 3.0.0** | Web framework |
| **MongoDB 7.0** | NoSQL database |
| **PyJWT** | JWT token handling |
| **bcrypt** | Password hashing |
| **Flasgger** | Swagger/OpenAPI documentation |
| **pytest** | Testing framework |
| **Flask-PyMongo** | MongoDB integration |
| **python-dotenv** | Environment variable management |

```
## 🚀 Quick Start

# Clone the repository
```commandline
git clone https://github.com/Mritunjoy99/task-manager-api.git

cd task-manager-api
```

# Create and activate virtual environment
```commandline
python3 -m venv venv
source venv/bin/activate
```
```commandline
# venv\Scripts\activate  # Windows
```

# Install dependencies
```commandline
pip install -r requirements.txt
```

# Set up environment variables
```commandline
cp .env.example .env
```
# Edit .env with your configuration

# Start MongoDB
```commandline
sudo systemctl start mongod
```

# Run the application
```commandline
python run.py
```
**Access the API:**
- **Base URL:** `http://localhost:5000/api`
- **Swagger Docs:** `http://localhost:5000/docs`

## 📦 Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **MongoDB 7.0+** - [Install MongoDB](https://www.mongodb.com/docs/manual/installation/)
- **pip** - Python package manager
- **Git** - Version control

### Step 1: Install MongoDB (Ubuntu/Debian)

```commandline
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update package list
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
sudo systemctl status mongod
```

### Step 2: Clone and Setup Project

```commandline
# Clone repository
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Configuration

```commandline
# Copy example environment file
cp .env.example .env

# Generate secure keys
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))" >> .env
```

Edit `.env` file:

```
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/task_manager

# Security Keys (IMPORTANT: Change these!)
SECRET_KEY=your-generated-secret-key-here
JWT_SECRET_KEY=your-generated-jwt-secret-key-here

# JWT Settings
JWT_ACCESS_TOKEN_EXPIRES=3600

# Environment
FLASK_ENV=development
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/task_manager` | ✅ |
| `SECRET_KEY` | Flask secret key | - | ✅ |
| `JWT_SECRET_KEY` | JWT signing key | - | ✅ |
| `JWT_ACCESS_TOKEN_EXPIRES` | Token lifetime (seconds) | `3600` | ❌ |
| `FLASK_ENV` | Environment mode | `development` | ❌ |

### Database Indexes

The application automatically creates these indexes for optimization[web:6][web:37]:

```
users.username (unique)
users.email (unique)
tasks.user_id
tasks.created_at
```

## Usage

### Starting the Development Server

```
# Ensure MongoDB is running
sudo systemctl status mongod

# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

The server will start at `http://localhost:5000`

### Using Swagger UI

1. Navigate to `http://localhost:5000/docs`
2. Click on any endpoint to expand it
3. For protected endpoints:
   - First, register/login to get a JWT token
   - Click **"Authorize"** button (🔓 icon)
   - Enter: `Bearer YOUR_TOKEN_HERE`
   - Click **"Authorize"**
4. Now you can test all endpoints interactively

### Using cURL

#### Register a New User

```
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```
{
  "message": "User created successfully",
  "user_id": "673f1a8b9c1d4e5f6a7b8c9d"
}
```

#### Login

```
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

**Response:**
```
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "673f1a8b9c1d4e5f6a7b8c9d",
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2025-11-09T15:30:00.000Z"
  }
}
```

#### Create a Task

```
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write comprehensive README and API docs"
  }'
```

#### Get All Tasks (with Pagination)

```
# Get first page (10 items)
curl -X GET "http://localhost:5000/api/tasks?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get completed tasks only
curl -X GET "http://localhost:5000/api/tasks?completed=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update a Task

```
curl -X PUT http://localhost:5000/api/tasks/TASK_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated title",
    "completed": true
  }'
```

#### Delete a Task

```
curl -X DELETE http://localhost:5000/api/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🌐 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register` | Register new user | ❌ |
| `POST` | `/api/auth/login` | Login and get JWT | ❌ |

### Tasks

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/tasks` | Get all tasks (paginated) | ✅ |
| `GET` | `/api/tasks/{id}` | Get specific task | ✅ |
| `POST` | `/api/tasks` | Create new task | ✅ |
| `PUT` | `/api/tasks/{id}` | Update task | ✅ |
| `DELETE` | `/api/tasks/{id}` | Delete task | ✅ |

### Query Parameters

**GET /api/tasks**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `page` | integer | Page number | `1` |
| `per_page` | integer | Items per page | `10` |
| `completed` | boolean | Filter by status | `null` |

## 🧪 Testing

### Run Tests

```
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v
pytest tests/test_tasks.py -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/
```

### Test Coverage

```
tests/test_auth.py::test_register_user ✓
tests/test_auth.py::test_register_duplicate_username ✓
tests/test_auth.py::test_login_success ✓
tests/test_auth.py::test_login_invalid_credentials ✓
tests/test_auth.py::test_missing_fields_register ✓
tests/test_tasks.py::test_create_task ✓
tests/test_tasks.py::test_get_all_tasks ✓
tests/test_tasks.py::test_get_task_by_id ✓
tests/test_tasks.py::test_update_task ✓
tests/test_tasks.py::test_delete_task ✓
tests/test_tasks.py::test_unauthorized_access ✓
tests/test_tasks.py::test_pagination ✓
tests/test_tasks.py::test_filter_by_completed ✓

========== 13 passed in 2.45s ==========
Coverage: 95%
```

## Project Structure

```
task-manager-api/
│
├── app/
│   ├── __init__.py              # App factory & config
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Flask extensions (PyMongo)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model & operations
│   │   └── task.py              # Task model & operations
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Auth endpoints (register/login)
│   │   └── tasks.py             # Task CRUD endpoints
│   │
│   └── utils/
│       ├── __init__.py
│       └── decorators.py        # JWT auth decorators
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_auth.py             # Auth endpoint tests
│   └── test_tasks.py            # Task endpoint tests
│
├── .env                         # Environment variables (git-ignored)
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## 🚀 Deployment

### Production with Gunicorn + Nginx

#### 1. Install Gunicorn

```
pip install gunicorn
```

#### 2. Create systemd Service

Create `/etc/systemd/system/taskmanager.service`:

```
[Unit]
Description=Task Manager API
After=network.target mongodb.service

[Service]
User=youruser
Group=www-data
WorkingDirectory=/path/to/task-manager-api
Environment="PATH=/path/to/task-manager-api/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/path/to/task-manager-api/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:5000 \
    --access-logfile /var/log/taskmanager/access.log \
    --error-logfile /var/log/taskmanager/error.log \
    "app:create_app('production')"

Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3. Start Service

```
# Create log directory
sudo mkdir -p /var/log/taskmanager
sudo chown youruser:www-data /var/log/taskmanager

# Start and enable service
sudo systemctl daemon-reload
sudo systemctl start taskmanager
sudo systemctl enable taskmanager
sudo systemctl status taskmanager
```

#### 4. Configure Nginx

Create `/etc/nginx/sites-available/taskmanager`:

```
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

Enable and restart Nginx:

```
sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL with Let's Encrypt

```
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

## 🔧 Troubleshooting

### MongoDB Not Starting

```
# Check status
sudo systemctl status mongod

# View logs
sudo journalctl -u mongod

# Restart service
sudo systemctl restart mongod
```

### Port Already in Use

```
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>
```

### Import Errors

```
# Deactivate and recreate virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### MongoDB Connection Failed

Check your `MONGO_URI` in `.env`:
```
# Correct format
MONGO_URI=mongodb://localhost:27017/task_manager

# If using authentication
MONGO_URI=mongodb://username:password@localhost:27017/task_manager
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines[web:31][web:35]:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Coding Standards

- Follow [PEP 8](https://pep8.org/) style guide
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR


## 👨‍💻 Author

**Mritunjoy Kumar Yadav**

- GitHub: [@Mritunjoy99](https://github.com/Mritunjoy99)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/) - Excellent web framework
- [MongoDB Documentation](https://docs.mongodb.com/) - Comprehensive database docs
- [Flasgger](https://github.com/flasgger/flasgger) - Swagger integration for Flask
- [pytest](https://docs.pytest.org/) - Testing framework

## 📞 Support

If you encounter any issues or have questions:

- **Open an Issue**: [GitHub Issues](https://github.com/Mritunjoy99/task-manager-api/issues)
- **Email**: support@example.com
- **Documentation**: Check `/docs` endpoint for API reference

## 🗺️ Roadmap

- [ ] Add email verification for new users
- [ ] Implement task categories/tags
- [ ] Add task priority levels
- [ ] Include task due dates and reminders
- [ ] Add task sharing between users
- [ ] Implement WebSocket for real-time updates
- [ ] Add export functionality (CSV, JSON)
- [ ] Create admin dashboard

---

**Made with ❤️ by [Mritunjoy Kumar Yadav](https://github.com/Mritunjoy99)**

**⭐ Star this repo if you find it helpful!**

---

