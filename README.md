# Doctor Appointment Booking System

# Project Overview

 A comprehensive Django REST Framework API for managing doctor appointments. This system provides secure JWT authentication, role-based access control, and automated email notifications for patients, doctors, and administrators.

# 🚀 Features

 JWT Authentication - Secure user registration and login

 Role-Based Access - Patients, Doctors, and Administrators

 Appointment Management - Book, confirm, reject, and cancel appointments

 Email Notifications - Automated emails for appointment status changes

 Doctor Availability - Real-time availability checking

 Admin Dashboard - Comprehensive user and appointment management

 API Documentation - Swagger/OpenAPI documentation


# 🛠️ Tech Stack

 Backend: Django + Django REST Framework

 Database: MySQL (Production)

 Authentication: JWT Tokens (Simple JWT)

 Email: Mailtrap (Development), Gmail SMTP (Production)

 Documentation: Swagger/OpenAPI with drf-yasg


# 📋 Prerequisites

 Before you begin, ensure you have the following installed:

 Python 3.8 or higher

 MySQL Server

 Git


# 🚀 Quick Start

# 1. Clone the Repository

  bash
 git clone https://github.com/Chidera001-dev/doctor-appointment-system.git

 cd doctor-appointment-system


# 2. Set Up Virtual Environment
bash
 Create virtual environment
python -m venv venv

 Activate virtual environment
 On Windows:
venv\Scripts\activate
 On macOS/Linux:
source venv/bin/activate


# 3. Install Dependencies
bash
pip install -r requirements.txt

# 4. Set Up Environment Variables
Copy the example environment file and configure it:

bash
 Copy the example environment file
cp .env.example .env

# 5. Start with Docker Compose
bash
 Build and start all services
docker-compose up --build

 Or run in detached mode
docker-compose up -d --build

# 6. Run Database Migrations
bash
 Run migrations in the Docker container
 Run migrations
docker-compose exec (service-name) python manage.py makemigrations
docker-compose exec (service-name) python manage.py migrate

# 7. Create Superuser
bash
 Create admin user in the Docker container
docker-compose exec (service-name) python manage.py createsuperuser

 Follow the prompts to create an admin account:
 Username: admin
 Phone_number : +234****
 Email: admin@example.com
 Password: ***** 

# 8. Access the Application
Your application is now running! Access it at:

Authentication : http://localhost:8000/auth/

API: http://localhost:8000/api/

Admin Panel: http://localhost:8000/admin/

API Documentation: http://localhost:8000/docs/

MySQL Database: localhost:3306

# 📚 API Documentation
# Access API Documentation
Swagger UI: http://localhost:8000/docs/

ReDoc: http://localhost:8000/redoc/


# 🔐 Authentication Endpoints
# Base URL: http://localhost:8000/auth/


# 👨‍⚕️ Doctor Management Endpoints
# Base URL: http://localhost:8000/api/

# Register User
POST :   localhost:8000/auth/signup/


{
  "username": "john",
  "email": "john@gmail.com",
  "phone_number": "+2349057928312",
  "password": "johnpass123#"
}

# register doctor
POST :   localhost:8000/auth/signup/
{
  "username": "drjames",
  "email": "drjames@gmail.com",
  "phone_number": "+2348109378342",
  "password": "drjamespass123#"
}

# input your valid access key
POST : localhost:8000/auth/token/
{
 
  "email": "drjames@gmail.com",
  "password": "drjamespass123#"
}

POST : localhost:8000/api/doctors/create/
{
  "user": "",
  "specialization": "Cardiologist",
  "experience_years": 10,
  "available_days": "Mon, Wed, Fri",
  "available_time_slots": "09:00-14:00"
}

# user can view the list of available doctors
# input your valid access key
POST : localhost:8000/auth/token/
{
  
  "email": "drjames@gmail.com",
  "password": "drjamespass123#"
}


GET : localhost:8000/api/doctors/

# retrieve a particular doctors uuid

GET : localhost:8000/api/doctors/<doctor_id>/


# Appointment
users can also create appointment

POST : localhost:8000/api/appointments/

{
    "doctor_id": "",
    "date": "2025-10-17",
    "time": "11:00"
}

update or delete the appointment

PUT : localhost:8000/api/appointments/<appointment_id>/

DELETE : localhost:8000/api/appointments/<appointment_id>/


# doctors get all appointment assign to them 
# input your valid access key
POST : localhost:8000/auth/token/
{
 
  "email": "drjames@gmail.com",
  "password": "drjamespass123#"
}

GET : localhost:8000/api/appointments/<appointment_id>/

# doctors confirm or reject the appointment

PATCH : localhost:8000/api/appointments/status/

{
    "status" : "confirmed"
}

# USER MANAGEMENT (Admin)

Endpoints for creating and managing users (patients and doctors).
# input your valid access key
POST : localhost:8000/auth/token/
{
    "email" : "adminuser@gmail.com",
    "password" : "Chidera123"
}

Admin users can create users or doctors

POST : localhost:8000/api/admin/users/

{
  "username": "user10
  "email": "user10@gmail.com",
  "phone_number": "+2349057928555",
  "password": "userpass10"
}

views the list of doctors and patient

GET : localhost:8000/api/admin/users/

also can get Single User
GET : localhost:8000/api/admin/users/<user_id>/

can also Update User
PUT : localhost:8000/api/admin/users/<user_id>/

can also Delete user
DELETE : api/admin/users/<user_id>/






