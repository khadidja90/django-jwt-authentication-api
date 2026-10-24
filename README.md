# Django JWT Authentication API

A secure REST API built with **Django REST Framework** and **Simple JWT**. This project implements user registration, secure password storage, JWT-based login, protected endpoints, token refresh, and token verification.

It was developed as a backend authentication challenge to demonstrate the fundamentals of securing REST APIs.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [How Authentication Works](#how-authentication-works)
- [API Endpoints](#api-endpoints)
- [Installation and Setup](#installation-and-setup)
- [API Usage](#api-usage)
- [Running the Tests](#running-the-tests)
- [Security Considerations](#security-considerations)

## Overview

The purpose of this project is to implement a secure authentication system using Django REST Framework.

Users can create accounts, authenticate with their credentials, receive JSON Web Tokens (JWTs), and access protected resources. The API validates tokens before granting access to authenticated endpoints.

Django's built-in user model and password hashing mechanisms are used to avoid implementing password storage and cryptographic operations from scratch.

## Features

- **User registration:** Create accounts using a username, email, and password.
- **Password hashing:** Store passwords securely using Django's built-in password hashing.
- **Input validation:** Validate user data and enforce configured password requirements.
- **Duplicate email prevention:** Reject registration attempts using an already registered email.
- **JWT authentication:** Issue access and refresh tokens after successful login.
- **Protected endpoints:** Restrict profile access to authenticated users.
- **Token verification:** Validate JWTs using Simple JWT.
- **Token refresh:** Obtain a new access token using a valid refresh token.
- **Automated testing:** Test successful requests and authentication failures.
- **Browsable API:** Explore endpoints through Django REST Framework's browser interface.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend web framework |
| Django REST Framework | REST API development |
| Simple JWT | JWT issuing and verification |
| SQLite | Development database |
| Django Test Framework | Automated testing |

## Project Structure

```text
secure-auth-api/
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── README.md
└── requirements.txt
```

- `config/settings.py`: Project settings, password validation, and authentication configuration.
- `config/urls.py`: Main URL configuration.
- `accounts/serializers.py`: Signup data validation and user creation.
- `accounts/views.py`: Signup and protected profile endpoints.
- `accounts/urls.py`: API endpoint definitions.
- `accounts/tests.py`: Automated authentication tests.
- `accounts/models.py`: Uses Django's built-in user model; no custom model is required.

## How Authentication Works

### 1. Registration

The client sends a username, email, and password to the signup endpoint. Django validates the submitted data and hashes the password before storing the user.

### 2. Login

The client submits valid credentials. Simple JWT verifies the credentials and returns an access token and a refresh token.

### 3. Accessing Protected Resources

The client sends the access token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

Django REST Framework verifies the token's signature and expiration before allowing access to protected resources.

### 4. Token Refresh

When an access token expires, the client can submit a valid refresh token to obtain another access token.

### 5. Token Verification

The verification endpoint checks whether a submitted token is valid. Protected endpoints still perform their own authentication checks.

## API Endpoints

The API uses the `/api/` prefix.

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/signup/` | Register a new user | Public |
| POST | `/api/login/` | Obtain access and refresh tokens | Public |
| POST | `/api/token/refresh/` | Obtain a new access token | Refresh token required |
| POST | `/api/token/verify/` | Verify a token | Token supplied in request body |
| GET | `/api/profile/` | Retrieve the authenticated user's profile | Required |

### Typical Responses

| Scenario | Expected status |
|---|---|
| Successful signup | `201 Created` |
| Invalid signup data | `400 Bad Request` |
| Successful login | `200 OK` |
| Incorrect login credentials | `401 Unauthorized` |
| Profile request without valid authentication | `401 Unauthorized` |
| Successful profile request | `200 OK` |
| Invalid token verification | `401 Unauthorized` |

## Installation and Setup

### Prerequisites

- Python 3.10 or later, compatible with the installed Django version.
- pip.
- Windows CMD, PowerShell, or a terminal on another operating system.

### 1. Clone the repository

Replace the placeholder with your GitHub repository URL:

```bash
git clone https://github.com/YOUR_USERNAME/django-jwt-authentication-api.git
cd django-jwt-authentication-api
```

### 2. Create a virtual environment

On Windows CMD:

```cmd
py -m venv venv
venv\Scripts\activate.bat
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If `requirements.txt` is present:

```bash
python -m pip install -r requirements.txt
```

Otherwise, install the packages directly:

```bash
python -m pip install django djangorestframework djangorestframework-simplejwt
```

### 4. Configure the application

Review `config/settings.py`.

Ensure that `rest_framework` and `accounts` are included in `INSTALLED_APPS`, and that JWT authentication is configured.

For local development, SQLite is used by default.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator (optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 7. Start the development server

```bash
python manage.py runserver
```

The API is now available at:

http://127.0.0.1:8000/

The Django admin interface is available at:

http://127.0.0.1:8000/admin/

## API Usage

The following examples use `curl`. You can also inspect the endpoints through the Django REST Framework browsable API.

### 1. Register a User

**Request**

```http
POST /api/signup/
Content-Type: application/json
```

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "Replace-With-A-Strong-Password-482!"
}
```

**Expected response — `201 Created`**

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com"
}
```

The password is not returned in the response.

### 2. Log In

**Request**

```http
POST /api/login/
Content-Type: application/json
```

```json
{
  "username": "alice",
  "password": "Replace-With-A-Strong-Password-482!"
}
```

**Expected response — `200 OK`**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

The returned token values are placeholders. The actual values are generated by the server.

### 3. Access the User Profile

**Request**

```http
GET /api/profile/
Authorization: Bearer <access_token>
```

**Expected response — `200 OK`**

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com"
}
```

Requests without a valid access token should be rejected.

### 4. Refresh an Access Token

**Request**

```http
POST /api/token/refresh/
Content-Type: application/json
```

```json
{
  "refresh": "<refresh_token>"
}
```

**Expected response — `200 OK`**

```json
{
  "access": "<new_access_token>"
}
```

### 5. Verify a Token

**Request**

```http
POST /api/token/verify/
Content-Type: application/json
```

```json
{
  "token": "<access_token>"
}
```

A valid token normally returns `200 OK` with an empty response body. An invalid or expired token is rejected.

## Running the Tests

Run the complete authentication test suite:

```bash
python manage.py test accounts
```

Django creates a temporary test database, runs the tests, and destroys the database afterward.

The test suite covers:

- User registration and password hashing.
- Duplicate email rejection.
- Weak password rejection.
- Successful login and token issuance.
- Invalid login credentials.
- Access restrictions on protected endpoints.
- Valid and invalid JWT authentication.
- Refresh token functionality.
- Token verification.

A successful run ends with `OK`. The number of tests depends on the current contents of `accounts/tests.py`.

## Security Considerations

- **Password storage:** Use Django's password hashing APIs; never store plaintext passwords.
- **Token lifetime:** Access tokens are configured to expire after 15 minutes, and refresh tokens after one day.
- **Signing secret:** Keep Django's `SECRET_KEY` private and load it from an environment variable in production.
- **HTTPS:** Use HTTPS when deploying the API publicly.
- **Input validation:** Validate all incoming data and reject invalid registration attempts.
- **Authentication:** Require valid authentication for private resources.
- **Login protection:** Add rate limiting to reduce brute-force attempts.
- **Token handling:** Never expose tokens in public repositories, logs, or screenshots.
- **Email uniqueness:** The signup serializer validates duplicate emails; production systems should also enforce database-level uniqueness if required.
- **Refresh-token security:** Consider refresh-token rotation and blacklisting.

JWTs are signed, not encrypted by default. Do not store passwords or other sensitive secrets in token payloads.

The current development settings, including `DEBUG = True` and the placeholder secret key, are not suitable for production deployment.


---

*This project was created for learning and demonstrating secure authentication concepts with Django REST Framework and JWT.*
