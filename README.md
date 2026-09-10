# Blog Management API

A mini blogging system built with **FastAPI** that allows authenticated users to create and manage blog posts, add comments, like/unlike posts, and receive email notifications.

## 🚀 Features

* User registration and login
* JWT-based authentication
* Secure password hashing using bcrypt
* Create, read, update, and delete blog posts
* Users can update/delete only their own posts
* Public access to view posts and comments
* Add comments to blog posts
* Like and unlike blog posts
* Prevent duplicate likes
* Email notifications for new comments
* Email notifications for new likes
* Input validation using Pydantic
* SQLite database with SQLAlchemy ORM
* Interactive Swagger API documentation

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Programming Language:** Python
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Authentication:** JWT
* **Password Hashing:** bcrypt
* **Validation:** Pydantic
* **API Testing:** Swagger UI
* **Email:** SMTP
* **Server:** Uvicorn

## 📂 Project Structure

```text
Blog_management/
│
├── app/
│   ├── core/
│   │   ├── email.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── like.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── like.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── like.py
│   │
│   ├── database.py
│   └── main.py
│
├── .gitignore
├── README.md
└── blog.db
```

> `blog.db` is excluded from Git using `.gitignore`.

## 🔐 Authentication

The API uses **JWT authentication**.

### Register

```http
POST /auth/register
```

Creates a new user and returns an access token.

### Login

```http
POST /auth/login
```

Authenticates the user and returns a JWT access token.

The token is used to access protected endpoints.

## 📝 Post APIs

| Method | Endpoint           | Description              |
| ------ | ------------------ | ------------------------ |
| POST   | `/posts/`          | Create a post            |
| GET    | `/posts/`          | Get all posts            |
| GET    | `/posts/mine`      | Get current user's posts |
| GET    | `/posts/{post_id}` | Get a specific post      |
| PUT    | `/posts/{post_id}` | Update own post          |
| DELETE | `/posts/{post_id}` | Delete own post          |

Only the owner of a post can update or delete it.

## 💬 Comment APIs

| Method | Endpoint                     | Description   |
| ------ | ---------------------------- | ------------- |
| POST   | `/posts/{post_id}/comments/` | Add a comment |
| GET    | `/posts/{post_id}/comments/` | View comments |

When a user comments on another user's post, an email notification is sent to the post owner.

## ❤️ Like APIs

| Method | Endpoint                 | Description   |
| ------ | ------------------------ | ------------- |
| POST   | `/posts/{post_id}/like/` | Like a post   |
| DELETE | `/posts/{post_id}/like/` | Unlike a post |

A user cannot like the same post more than once.

When a user likes another user's post, an email notification is sent to the post owner.

## 🗄️ Database

The application uses **SQLite** with **SQLAlchemy ORM**.

The database contains four main tables:

* `users`
* `posts`
* `comments`
* `likes`

### Users

Stores registered user information.

### Posts

Stores blog posts and their authors.

### Comments

Stores comments associated with posts and users.

### Likes

Stores likes associated with posts and users.

## 📧 Email Notifications

SMTP email notifications are implemented for:

* New comments on a user's post
* New likes on a user's post

SMTP credentials are configured through environment variables and are not stored in the source code.

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Pradeeshs14/Blog_Management.git
cd Blog_Management
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy python-jose passlib bcrypt email-validator
```

### 5. Configure email settings

Set the required SMTP environment variables:

```powershell
$env:SMTP_HOST="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
```

Do not commit your email password or app password to GitHub.

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## 📚 Swagger Documentation

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to:

* Register users
* Login
* Authorize with JWT
* Create and manage posts
* Add comments
* Like and unlike posts
* Test API responses

## 🧪 Testing

The API was tested using Swagger UI.

Testing includes:

* User registration
* User login
* JWT authorization
* Post CRUD operations
* Post ownership validation
* Comment creation and retrieval
* Like and unlike functionality
* Duplicate like validation
* Email notifications
* SQLite database operations

## 🔒 Security

* Passwords are stored as bcrypt hashes.
* JWT tokens protect authenticated endpoints.
* Post ownership is verified before update/delete operations.
* SMTP credentials are stored using environment variables.
* Database and virtual environment files are excluded from Git.

## 📌 Project Status

**Completed ✅**

The Blog Management API is functional and ready for demonstration and submission.

## 👨‍💻 Author

**Pradeesh S**

Built as a FastAPI backend project demonstrating authentication, database management, REST APIs, authorization, email notifications, and API testing.
