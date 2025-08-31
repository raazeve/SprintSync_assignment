# SprintSync Backend

A robust Django REST Framework backend for SprintSync, an AI-powered task management system designed for engineering teams. This backend provides a clean, well-documented API with JWT authentication, task management, and AI integration.

## 🚀 Live Demo

- **Backend API**: [https://sprintsync-backend.onrender.com](https://sprintsync-backend.onrender.com)
- **API Documentation**: [https://sprintsync-backend.onrender.com/api/schema/swagger-ui/](https://sprintsync-backend.onrender.com/api/schema/swagger-ui/)
- **Frontend Application**: [https://sprintsync.vercel.app](https://sprintsync.vercel.app)

## ✨ Features

- **JWT Authentication**: Secure user authentication with refresh token support
- **Task Management**: Full CRUD operations for tasks with status transitions
- **AI Integration**: OpenAI-powered daily planning suggestions
- **Structured Logging**: Comprehensive request/response logging with performance metrics
- **RESTful API**: Clean, well-documented API endpoints following REST conventions
- **Admin Interface**: Django admin panel for data management
- **Database**: Production-ready database with proper relationships

## 🛠️ Technology Stack

- **Framework**: Django 4.2 & Django REST Framework
- **Database**: RDBMS
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: DRF Spectacular (Swagger/OpenAPI)
- **AI Integration**: OpenAI API
- **Deployment**: Render (with Docker support)
- **Logging**: Structured JSON logging

## 📁 Project Structure


backend/
├── backend/ # Django project settings
│ ├── settings.py # Environment-based configuration
│ ├── middleware.py # Custom logging middleware
│ ├── urls.py # Main URL routing
│ └── wsgi.py # WSGI application entrypoint
├── core/ # Main application
│ ├── models.py # Database models (User, Task)
│ ├── serializers.py # DRF serializers
│ ├── views.py # API views and viewsets
│ ├── urls.py # App-specific URL routing
├── Dockerfile # Container configuration
├── docker-compose.yml # Local development setup
├── requirements.txt # Python dependencies
└── manage.py # Django management script

text

## 🔧 Installation & Setup

### Prerequisites

- Python 3.10+
- DBMBS
- OpenAI API key (for AI features)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/raazeve/SprintSync_assignment.git
   cd SprintSync/backend
Create a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt

Set up the database

bash
python manage.py migrate
python manage.py createsuperuser
Run the development server

bash
python manage.py runserver
Docker Development
Build and start containers

bash
docker-compose up --build
Run migrations

bash
docker-compose exec web python manage.py migrate
Create a superuser

bash
docker-compose exec web python manage.py createsuperuser
📚 API Documentation
Once the server is running, access the API documentation at:

Swagger UI: /api/schema/swagger-ui/

ReDoc: /api/schema/redoc/

Raw OpenAPI Schema: /api/schema/

Key Endpoints
POST /api/auth/token/ - Obtain JWT tokens

POST /api/auth/token/refresh/ - Refresh access token

GET /api/tasks/ - List/create tasks

GET /api/tasks/{id}/ - Retrieve/update/delete task

PATCH /api/tasks/{id}/status/ - Update task status

POST /api/ai/daily_plan/ - Get AI-generated daily plan

🔐 Authentication
The API uses JWT authentication. Include the access token in the Authorization header:

http
Authorization: Bearer <your_access_token>
To obtain tokens:

Make a POST request to /api/auth/token/ with username and password

Use the returned access token for subsequent requests

Refresh the access token using the refresh token at /api/auth/token/refresh/