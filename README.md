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

API: http://localhost:8000/

Admin Panel: http://localhost:8000/admin/

API Documentation: http://localhost:8000/docs/

MySQL Database: localhost:3306

# 📚 API Documentation
# Access API Documentation
Swagger UI: http://localhost:8000/docs/

ReDoc: http://localhost:8000/redoc/

JSON Schema: http://localhost:8000/swagger.json

# 🔐 Authentication Endpoints
# Base URL: http://localhost:8000/auth/

# Method	Endpoint	Description	Access

POST	/auth/signup/	User registration	Public

POST	/auth/token/	Get JWT token (login)	Public

POST	/auth/token/refresh/	Refresh JWT token	Authenticated

POST	/auth/token/verify/	Verify JWT token	Authenticated


# 👨‍⚕️ Doctor Management Endpoints
# Base URL: http://localhost:8000/api/

Method	Endpoint	Description	Access

GET	/api/doctors/	List all doctors	Public

POST	/api/doctors/create/	Create doctor profile	Admin Only

GET	/api/doctors/{uuid}/	Get doctor details	Public

PUT	/api/doctors/{uuid}/update/	Update doctor profile	Admin/Doctor

DELETE	/api/doctors/{uuid}/delete/	Delete doctor profile	Admin Only

# 📅 Appointment Management Endpoints

# Base URL: `http://localhost:8000/api/**

Method	Endpoint	Description	Access

GET	/api/appointments/	List appointments	Role-based

POST	/api/appointments/	Book appointment	Patients Only

GET	/api/appointments/{uuid}/	Get appointment details	Owner/Doctor/Admin

PUT	/api/appointments/{uuid}/	Update appointment	Owner/Doctor/Admin

DELETE	/api/appointments/{uuid}/	Cancel appointment	Patient Only

PUT	/api/appointments/{uuid}/status/	Update appointment status	Doctor/Admin

# 👑 Admin Management Endpoints

# Base URL: `http://localhost:8000/api/**

Method	Endpoint	Description	Access

GET	/api/admin/users/	List all users	Admin Only

POST	/api/admin/users/	Create new user	Admin Only

GET	/api/admin/users/{uuid}/	Get user details	Admin Only

PUT	/api/admin/users/{uuid}/	Update user	Admin Only

DELETE	/api/admin/users/{uuid}/	Delete user	Admin Only

# 📞 Support

# If you encounter any issues:

Check the troubleshooting section above

Ensure Docker Desktop is running

Verify your .env file configuration

Check container logs: docker-compose logs

 Visit API documentation: http://localhost:8000/docs/

# Access Points:

# API: http://localhost:8000/

# Admin: http://localhost:8000/admin/

# Docs: http://localhost:8000/docs/

Happy Coding with Docker! 🐳🚀
