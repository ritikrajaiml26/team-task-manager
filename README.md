# Team Task Manager

A full-stack project and task management system with Role-Based Access Control (RBAC), JWT Authentication, and real-time dashboards.

## 🚀 Features

- **Role-Based Access Control (RBAC):**
  - **Admin:** Can create projects, view global metrics (Total, Overdue, In Progress), assign tasks to any member, and monitor the progress of all users in the system.
  - **Member:** Can view personal dashboards, see tasks specifically assigned to them, and update the status of their tasks without modifying overarching project details.
- **Project & Task Tracking:** Organizes tasks securely under distinct projects to maintain clean workflows.
- **Dynamic Dashboards:** Real-time calculation of task statuses (To Do, In Progress, Completed, Overdue) and user progress percentages.
- **Secure Authentication:** Implements JWT (JSON Web Tokens) for fast, secure, and stateless authentication between the frontend and backend.

## 🛠️ Tech Stack

### Frontend
- HTML5 & CSS3 (Vanilla, custom dark-mode UI with CSS variables)
- JavaScript (Vanilla ES6+ using Fetch API)
- Responsive layout using CSS Grid and Flexbox

### Backend
- **Python 3.x**
- **Django 5.x**
- **Django Rest Framework (DRF)**
- **Simple JWT** (for Authentication)
- **django-cors-headers** (for Cross-Origin Resource Sharing)
- **SQLite** (Default DB, easily scalable to PostgreSQL)

## 💻 How to Run Locally

### 1. Backend Setup

Open a terminal and navigate to the root folder (where `manage.py` is located):

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver
```
*The backend API will run on `http://127.0.0.1:8000`.*

### 2. Frontend Setup

1. Open the `frontend` folder using a local web server (e.g., **Live Server** extension in VS Code).
2. Ensure the frontend is served on port `5500` (i.e., `http://127.0.0.1:5500`) or update the `CORS_ALLOWED_ORIGINS` in your backend `.env` file to match your live server URL.
3. Open `http://127.0.0.1:5500/admin-register.html` to create your first Admin account.

### 3. Environment Variables (`.env`)
Create a `.env` file in the same directory as your `manage.py` file to configure production/local settings:
```ini
DEBUG=True
SECRET_KEY=your_secure_django_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

## 🌍 Deployment on Railway

This repository is structured to be seamlessly deployed on Railway.

### Backend Deployment
1. Connect this repository to Railway.
2. Railway will automatically detect the `manage.py` file and deploy the Django server.
3. Set your Railway environment variables (`ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`).

### Frontend Deployment
1. Create a new service in your Railway project connecting to the exact same repository.
2. Go to the new service **Settings** -> **Root Directory** and type `frontend`.
3. Railway will serve your frontend statically.
4. (Optional) Generate a domain for your frontend in the **Networking** tab and update the backend's `CORS_ALLOWED_ORIGINS` variable to allow the new domain.
