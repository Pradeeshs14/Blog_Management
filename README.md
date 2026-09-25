# Blog Management API

A full-featured Blog Management API built using **FastAPI, SQLite, SQLAlchemy, JWT authentication, Auth0, Django Admin, Chart.js, and a responsive dashboard**.

The project provides blog management, comments, likes, subscriptions, billing, notifications, AI support, analytics, and multiple authentication methods.

---

# 1. Project Setup

* FastAPI backend created
* SQLite database configured
* SQLAlchemy ORM implemented
* Project structure organized into:

  * Models
  * Schemas
  * Routes
  * Services
  * Utilities
* Swagger API documentation available
* Responsive web dashboard implemented

---

# 2. Authentication

The application supports multiple authentication methods.

### Authentication Methods

* Email and password signup
* Email and password login
* JWT authentication
* Google login through Auth0
* Facebook login through Auth0
* Auth0 session handling
* Logout functionality
* Protected API authentication

### Password Security

* Passwords are hashed using bcrypt
* Passwords are never stored as plain text
* JWT access tokens are generated after successful authentication

---

# 3. 🔐 Auth0 & Social Authentication

Auth0 is integrated to provide social authentication through Google and Facebook.

### Auth0 Application

Application name:

```text
Blog Management Api
```

Auth0 domain:

```text
dev-mugvz3kei4finwuy.us.auth0.com
```

### Social Connections

Google:

```text
google-oauth2
```

Facebook:

```text
facebook-custom
```

### Auth0 Callback URL

For local development:

```text
http://127.0.0.1:8000/auth/callback/
```

### Allowed Web Origins

```text
http://127.0.0.1:8000
```

### Allowed Logout URL

```text
http://127.0.0.1:8000/
```

### Auth0 Environment Variables

The following configuration is stored in `.env`:

```env
AUTH0_DOMAIN=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_CALLBACK_URL=http://127.0.0.1:8000/auth/callback/
```

> Never commit `AUTH0_CLIENT_SECRET` or other sensitive credentials to GitHub.

---

# 4. Authentication API Endpoints

| Method | Endpoint                | Description                       |
| ------ | ----------------------- | --------------------------------- |
| POST   | `/auth/register`        | Register using email and password |
| POST   | `/auth/login`           | Login using email and password    |
| GET    | `/auth/signup/`         | Start Auth0 signup                |
| GET    | `/auth/login/google/`   | Login using Google                |
| GET    | `/auth/login/facebook/` | Login using Facebook              |
| GET    | `/auth/callback/`       | Auth0 callback                    |
| GET    | `/auth/session/`        | Retrieve Auth0 session token      |

---

# 5. Email Registration

Users can create an account using their name, email address, and password.

### Endpoint

```text
POST /auth/register
```

### Example Request

```json
{
  "name": "Test User",
  "email": "testuser@example.com",
  "password": "Test@123"
}
```

### Registration Process

```text
User
 ↓
Enter Name + Email + Password
 ↓
Validate Request
 ↓
Check Existing Email
 ↓
Hash Password
 ↓
Create User
 ↓
Generate JWT
 ↓
Dashboard
```

The email authentication provider is stored as:

```text
provider = email
```

---

# 6. Email Login

Registered users can log in using their email address and password.

### Endpoint

```text
POST /auth/login
```

### Example Request

```json
{
  "email": "testuser@example.com",
  "password": "Test@123"
}
```

### Login Process

```text
Email + Password
 ↓
Find User
 ↓
Verify Password
 ↓
Generate JWT
 ↓
Dashboard
```

Invalid credentials return:

```text
Invalid email or password
```

---

# 7. Google Login

Google authentication is handled through Auth0.

### Endpoint

```text
GET /auth/login/google/
```

### Google Login Flow

```text
Dashboard
 ↓
Google Login
 ↓
Auth0
 ↓
Google Authentication
 ↓
Auth0 Callback
 ↓
Create / Update Local User
 ↓
Generate Local JWT
 ↓
Dashboard
```

The Google provider is stored as:

```text
provider = google
```

---

# 8. Facebook Login

Facebook authentication is handled through Auth0.

### Endpoint

```text
GET /auth/login/facebook/
```

### Facebook Login Flow

```text
Dashboard
 ↓
Facebook Login
 ↓
Auth0
 ↓
Facebook Authentication
 ↓
Auth0 Callback
 ↓
Create / Update Local User
 ↓
Generate Local JWT
 ↓
Dashboard
```

The Facebook provider is stored as:

```text
provider = facebook
```

---

# 9. Auth0 Callback

The Auth0 callback endpoint is:

```text
GET /auth/callback/
```

The callback performs the following operations:

1. Receives the authorization code.
2. Validates Auth0 errors.
3. Exchanges the authorization code for an Auth0 access token.
4. Retrieves user information from Auth0.
5. Identifies the authentication provider.
6. Checks whether the user already exists.
7. Creates a new local user when required.
8. Updates an existing user's Auth0 information.
9. Generates a local JWT.
10. Stores the JWT in the application session.
11. Redirects the user to the dashboard.

### Auth0 User Data

The application stores:

```text
auth0_id
provider
email
name
username
```

---

# 10. User Model

The `users` table contains:

```text
id
username
email
password
name
provider
auth0_id
```

### Provider Values

```text
email
google
facebook
```

The `auth0_id` field stores the unique Auth0 identity for social-login users.

---

# 11. Authentication UI

The dashboard authentication interface provides:

* Email/password sign in
* JWT access-token login
* Email signup
* Google login
* Facebook login
* Logout
* Authentication error messages
* Responsive authentication interface
* Token management

---

# 12. Logout

The dashboard includes a logout button.

When logout is selected:

1. The active session is cleaned up.
2. The JWT is removed from browser storage.
3. The local authentication token is cleared.
4. The user is returned to the dashboard login screen.

---

# 13. Authentication Error Handling

The authentication system handles the following errors:

* Invalid email/password
* Existing email during registration
* Missing Auth0 authorization code
* Auth0 authentication failure
* Auth0 token exchange failure
* Missing Auth0 access token
* Missing Auth0 user ID
* Invalid social login provider
* Authentication session unavailable

---

# 14. Blog Posts

The Blog Management API provides complete post management.

### Features

* Create posts
* View posts
* Update posts
* Delete posts
* View user's own posts
* Post ownership validation
* Image support
* Post view tracking

---

# 15. Comments

### Features

* Add comments to posts
* View comments
* Comment validation
* Ownership-related validation
* Email notification to the post owner when a comment is added
* In-app comment notifications

---

# 16. Likes

### Features

* Like posts
* Unlike posts
* Duplicate like prevention
* Like validation
* Email notification to the post owner
* In-app like notifications

---

# 17. Subscription System

Three subscription plans are implemented:

| Plan    | Price |
| ------- | ----: |
| Basic   |   ₹99 |
| Premium |  ₹199 |
| Pro     |  ₹299 |

### Subscription Features

* 30-day subscriptions
* Post limits
* Image limits
* Like limits
* Comment limits
* Active subscription validation
* Subscription expiry handling
* Subscription renewal
* Billing history
* Invoice PDF generation

---

# 18. Subscription API Endpoints

| Method | Endpoint                                              | Description                      |
| ------ | ----------------------------------------------------- | -------------------------------- |
| GET    | `/subscriptions/plans`                                | Get available subscription plans |
| POST   | `/subscriptions/`                                     | Create a subscription            |
| POST   | `/subscriptions/renew`                                | Renew an active subscription     |
| GET    | `/subscriptions/me`                                   | Get current user's subscription  |
| GET    | `/subscriptions/billing-history`                      | Get billing history              |
| GET    | `/subscriptions/billing-history/{billing_id}/invoice` | Generate/view invoice            |

---

# 19. Email Notification System

SMTP-based email notifications are implemented.

### Notifications

* Comment notifications
* Like notifications
* Email testing completed successfully

---

# 20. 🔔 Notification Center

The application includes an in-app Notification Center with a notification bell.

### Notification Features

* Like notifications
* Comment notifications
* Subscription activation notifications
* Subscription renewal notifications
* Unread notification count
* Read/unread status
* Mark individual notification as read
* Mark individual notification as unread
* Mark all notifications as read
* Responsive notification dropdown
* JWT-protected notification APIs

### Notification Types

```text
like
comment
subscription
```

---

# 21. Notification API Endpoints

| Method | Endpoint                                  | Description                      |
| ------ | ----------------------------------------- | -------------------------------- |
| GET    | `/notifications/`                         | Get current user's notifications |
| GET    | `/notifications/unread-count`             | Get unread notification count    |
| PUT    | `/notifications/{notification_id}/read`   | Mark notification as read        |
| PUT    | `/notifications/{notification_id}/unread` | Mark notification as unread      |
| PUT    | `/notifications/read-all`                 | Mark all notifications as read   |

### Notification Testing

The following were tested:

* Notification bell
* Notification dropdown
* Like notifications
* Comment notifications
* Subscription notifications
* Unread notification count
* Mark as read
* Mark as unread
* Mark all as read

---

# 22. 🤖 AI Support Chat

The dashboard includes an AI Support Chat feature for authenticated users.

### Features

* Floating AI Support button
* Responsive chat interface
* User message input
* AI response display
* Scrollable conversation history
* Persistent chat history
* User-specific chat history
* JWT-protected APIs
* Database conversation tracking
* Responsive dashboard integration

### Supported Topics

* Creating posts
* Editing posts
* Deleting posts
* Subscription management
* Billing information
* Profile management
* Dashboard analytics
* General platform FAQs

---

# 23. AI Support API Endpoints

| Method | Endpoint           | Description                                        |
| ------ | ------------------ | -------------------------------------------------- |
| GET    | `/api/ai-support/` | Get current user's AI support chat history         |
| POST   | `/api/ai-support/` | Send a question and receive an AI support response |

### Stored Conversation Data

Each conversation stores:

```text
User ID
User Question
AI Response
Created Timestamp
```

### AI Response System

The current implementation uses predefined FAQ-based responses instead of an external AI service.

The backend:

1. Receives the user's question.
2. Processes it through the FAQ response system.
3. Returns the appropriate response.
4. Stores the conversation in the database.

---

# 24. Dashboard & Analytics

The dashboard provides authenticated users with their own blog statistics.

### Dashboard Statistics

* Total posts
* Comments made
* Likes received
* Total post views

### Analytics Charts

Interactive Chart.js charts display:

* Likes per post
* Comments per post

Users only receive analytics related to their own posts.

---

# 25. Post View Tracking

Post view tracking is implemented using the `views` field.

### Features

* Post views are tracked
* Each post view increments the count
* Total views are displayed on the dashboard
* User-specific view analytics are displayed

---

# 26. Dashboard UI

The dashboard includes:

* Responsive layout
* Dark-mode interface
* Statistics cards
* Chart.js analytics
* JWT-based API data loading
* Mobile-responsive design
* Access Token management
* Authentication interface
* Google login
* Facebook login
* Email login
* Email signup
* Notification Center
* Toast notifications
* AI Support Chat
* Logout functionality

---

# 27. Django Admin

A Django admin project is integrated into the application.

### Admin Features

* Subscription plan management
* Billing information management
* Administrative data management

---

# 28. Testing

The following features have been tested.

## Authentication

* User registration
* Email/password login
* JWT authentication
* Protected APIs
* Auth0 authentication
* Google login
* Facebook login
* Auth0 callback
* User creation/update
* Logout

## Blog Features

* Post creation
* Post retrieval
* Post update
* Post deletion
* Post ownership validation
* Image support
* Post view tracking

## Comments & Likes

* Comment creation
* Comment retrieval
* Comment validation
* Like functionality
* Unlike functionality
* Duplicate-like prevention

## Notifications

* Email notifications
* In-app Notification Center
* Like notifications
* Comment notifications
* Subscription notifications
* Read/unread functionality
* Mark all as read

## Subscriptions & Billing

* Subscription plans
* Subscription creation
* Active subscription validation
* Subscription renewal
* Subscription expiry
* Billing history
* Invoice generation

## Dashboard

* Dashboard statistics
* Likes analytics
* Comments analytics
* Post view tracking
* JWT-based dashboard access
* Responsive dashboard UI

## AI Support

* AI Support chat interface
* FAQ-based responses
* Create post assistance
* Edit post assistance
* Delete post assistance
* Subscription assistance
* Billing assistance
* Profile assistance
* Dashboard analytics assistance
* Chat history
* Persistent chat history
* JWT-protected AI Support endpoints

---

# 29. Local Development

### Install Dependencies

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file and configure the required application settings.

Example Auth0 configuration:

```env
AUTH0_DOMAIN=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_CALLBACK_URL=http://127.0.0.1:8000/auth/callback/
```

Keep all secrets private.

### Start the Application

```powershell
uvicorn app.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Dashboard:

```text
http://127.0.0.1:8000/dashboard
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 30. Project Documentation

Additional Auth0 documentation is available in:

```text
AUTH0_DOCUMENTATION.md
```

The document covers:

* Auth0 application setup
* Google configuration
* Facebook configuration
* Callback URL
* Allowed Web Origins
* Allowed Logout URLs
* Environment variables
* Authentication flow
* Local testing
* Error handling
* Security considerations

---

# 31. Project Structure

```text
Blog_management/
│
├── app/
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── static/
│   │   └── dashboard.html
│   ├── database.py
│   └── main.py
│
├── django_admin/
│
├── AUTH0_DOCUMENTATION.md
├── README.md
├── requirements.txt
├── .env
└── .gitignore
```

---

# 32. GitHub

Project source code:

`https://github.com/Pradeeshs14/Blog_Management.git`

The repository contains the FastAPI backend, dashboard, authentication implementation, subscription system, notification system, AI Support system, and project documentation.
