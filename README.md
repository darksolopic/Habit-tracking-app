# Habit Tracker API (Production Ready Backend)

Live API: [https://habit-tracker-em2l.onrender.com](https://habit-tracker-em2l.onrender.com)
API Documentation (Swagger): [https://habit-tracker-em2l.onrender.com/docs](https://habit-tracker-em2l.onrender.com/docs)
GitHub Repository: [https://github.com/darksolopic/Habit-tracking-app](https://github.com/darksolopic/Habit-tracking-app)

---

## Project Overview

Habit Tracker API is a production-ready backend application built using FastAPI and PostgreSQL.
It allows users to register, authenticate using JWT, create habits, mark them as completed, and view a dashboard summary.

This project demonstrates:

* REST API development
* Authentication using JWT
* Secure password hashing
* Database modeling with SQLAlchemy
* PostgreSQL integration (Supabase)
* Production deployment (Render)
* Environment variable management

---

## Tech Stack

Backend Framework: FastAPI
Database: PostgreSQL (Supabase)
ORM: SQLAlchemy
Authentication: JWT (python-jose)
Password Hashing: Passlib (bcrypt)
Deployment: Render
Version Control: Git & GitHub

---

## Authentication Flow

1. User registers using email and password

2. Password is securely hashed using bcrypt

3. User logs in

4. Server generates JWT access token

5. Token must be included as:

   Authorization: Bearer <access_token>

6. Protected routes validate the token before granting access

---

## API Endpoints

### Public Endpoints

POST /register
Register a new user

POST /login
Authenticate user and receive JWT token

GET /
Health check endpoint

---

### Protected Endpoints (Require JWT)

GET /habits
Retrieve all habits for logged-in user

POST /habits
Create a new habit

POST /habits/{habit_id}/complete
Mark habit as completed for the day

GET /dashboard
View summary statistics of user habits

---

## 🗄 Database Structure

### Users Table

* id (Primary Key)
* email (Unique)
* hashed_password

### Habits Table

* id (Primary Key)
* title
* owner_id (Foreign Key → Users)

### Completions Table

* id (Primary Key)
* habit_id (Foreign Key)
* date
* Unique constraint on (habit_id, date)

---

## How It Works (Execution Flow)

1. FastAPI starts using Uvicorn
2. SQLAlchemy connects to PostgreSQL using DATABASE_URL
3. Tables are created automatically if not present
4. Client sends HTTP request
5. FastAPI validates request using Pydantic schemas
6. Database operation is executed
7. JSON response returned to client

---

## Deployment Details

The application is deployed on Render using:

Build Command:

pip install -r requirements.txt

Start Command:

uvicorn app.main:app --host 0.0.0.0 --port 10000

Environment Variables configured securely in Render:

DATABASE_URL
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES

---

## Continuous Deployment

This project is connected to GitHub.

Whenever code is pushed to the main branch:

1. Render automatically rebuilds the project
2. New version is deployed
3. Same public URL reflects updated changes

---

## Testing the API

Use Swagger UI:

[https://habit-tracker-em2l.onrender.com/docs](https://habit-tracker-em2l.onrender.com/docs)

Steps:

1. Register a user
2. Login to receive JWT token
3. Click "Authorize" and paste token
4. Access protected routes

---

## Future Improvements

* Frontend UI (React)
* Habit streak tracking
* Analytics dashboard
* Role-based access control
* Docker containerization
* CI/CD pipeline

---

## Purpose of This Project

This project was built to demonstrate backend engineering skills including:

* API architecture
* Authentication & authorization
* Database schema design
* Secure credential handling
* Production deployment

It is suitable for:

* Backend Developer portfolio
* Technical interviews
* Full-stack project foundation

---

## Author

Gautam Sinha
Backend Developer
GitHub: [https://github.com/darksolopic](https://github.com/darksolopic)

---

⭐ If you find this project useful, consider giving it a star on GitHub.

