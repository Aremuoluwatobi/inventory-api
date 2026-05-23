Inventory Management API (Flask + PostgreSQL + JWT + AI Categorization)

Overview
This is a backend system for managing inventory. It includes admin authentication, inventory CRUD operations, and AI-based categorization using Ollama (LLaMA 3.1).

Features

Authentication
- Admin registration
- Admin login
- JWT-based authentication

Inventory Management
- Add inventory item
- Get inventory by ID
- Get inventory by date
- Update inventory
- Delete inventory

AI Feature
- Automatic categorization of inventory items using LLaMA 3.1

Tech Stack
- Python (Flask)
- PostgreSQL
- JWT
- bcrypt
- psycopg2
- Ollama (LLaMA 3.1)

Project Structure
conn.py
main.py
crud.py
ai_function.py
validation.py


Environment Variables
SECRET_KEY=your_secret_key

Setup Instructions

1. Download the project from GitHub.

2. Install the required packages:

pip install flask psycopg2-binary bcrypt pyjwt requests

Required packages:
Flask, psycopg2-binary, bcrypt, pyjwt, requests

3. Set up PostgreSQL database and create the required tables.

4. Create your own environment variable:

SECRET_KEY=your_random_secret_key

5. Run the application:

python main.py

API Endpoints

Auth
POST /register
POST /login

Inventory
POST /inventory
GET /inventory/<id>
GET /inventory?date_added=...
PUT /inventory/<id>
DELETE /inventory/<id>

AI
POST /ai-categorize

Testing

Use Postman to test endpoints.

Protected routes require:

Authorization: Bearer <token>

Example Request (Register)

- POST /register

{
  "user_name": "testuser",
  "email": "test@gmail.com",
  "password": "1234"
}

Example Request (Login)

- POST /login

{
  "email": "test@gmail.com",
  "password": "1234"
}

Example Request (Inventory)

- POST /inventory

{
  "name": "Rice",
  "quantity": 5,
  "price": 2000,
  "date_added": 2026
}

Header:

Authorization: Bearer <token>

Future Improvements

- Add inventory history tracking
- Add low-stock alerts
- Add a simple frontend dashboard
- Improve inventory categorization with additional training data

Author
Aremu Oluwatobiloba