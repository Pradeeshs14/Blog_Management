# Blog Management API

A mini blogging system built with **FastAPI** that allows authenticated users to create and manage blog posts, add comments, like/unlike posts, upload post images, search and paginate posts, and receive email notifications.

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
* Image upload for blog posts
* Image update support for posts
* Images served through `/media/posts/`
* Search posts by title or content
* Pagination for posts
* Search and pagination can be used together
* Input validation using Pydantic
* SQLite database with SQLAlchemy ORM
* Interactive Swagger API documentation
* Postman API testing

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Programming Language:** Python
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Authentication:** JWT
* **Password Hashing:** bcrypt
* **Validation:** Pydantic
* **File Upload:** FastAPI UploadFile
* **API Testing:** Swagger UI, Postman
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
├── media/
│   └── posts/
│       └── uploaded images
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

| Method | Endpoint           | Description                              |
| ------ | ------------------ | ---------------------------------------- |
| POST   | `/posts/`          | Create a post with optional image upload |
| GET    | `/posts/`          | Get posts with search and pagination     |
| GET    | `/posts/mine`      | Get current user's posts                 |
| GET    | `/posts/{post_id}` | Get a specific post                      |
| PUT    | `/posts/{post_id}` | Update own post with optional image      |
| DELETE | `/posts/{post_id}` | Delete own post                          |

Only the owner of a post can update or delete it.

### Image Upload

Posts support optional image uploads using multipart form data.

Uploaded images are stored under:

```text
/media/posts/
```

The API returns the image path in the post response.

Example:

```json
{
    "id": 4,
    "title": "image test",
    "content": "testing image",
    "author_id": 1,
    "created_at": "2026-09-15T06:27:59.738686",
    "image": "/media/posts/example-image.png"
}
```

The image can be accessed through:

```text
http://127.0.0.1:8000/media/posts/example-image.png
```

### Search

Posts can be searched using the `search` query parameter.

```http
GET /posts/?search=testing
```

Search is performed against:

* Post title
* Post content

### Pagination

Posts support pagination using `page` and `limit`.

```http
GET /posts/?page=1&limit=10
```

The response includes:

* `posts`
* `total`
* `page`
* `limit`
* `total_pages`

### Search + Pagination

Search and pagination can be used together.

```http
GET /posts/?search=testing&page=1&limit=2
```

Example response:

```json
{
    "posts": [],
    "total": 3,
    "page": 1,
    "limit": 2,
    "total_pages": 2
}
```

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

Stores blog posts, authors, and uploaded image paths.

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
pip install fastapi uvicorn sqlalchemy python-jose passlib bcrypt email-validator python-multipart
```

### 5. Configure email settings

Set the required SMTP environment variables:

```powershell
$env:SMTP_HOST="smtp.gmail.com"

$env:SMTP_PORT="587"

$env:SMTP_USERNAME="email@gmail.com"

$env:SMTP_PASSWORD="app-password"
```


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
* Create posts with image uploads
* Update posts with images
* Search posts
* Test pagination
* Test search with pagination
* Add comments
* Like and unlike posts
* Test API responses

## 🧪 Testing

The API was tested using **Swagger UI** and **Postman**.

Testing includes:

* User registration
* User login
* JWT authorization
* Post CRUD operations
* Post ownership validation
* Image upload
* Image update
* Image URL response
* Post pagination
* Post search by title/content
* Search and pagination together
* Comment creation and retrieval
* Like and unlike functionality
* Duplicate like validation
* Email notifications
* SQLite database operations

### Postman Testing

The Postman collection includes requests for:

* Login
* Create Post - Image Upload
* Get Posts - Pagination
* Search Posts
* Search + Pagination
* Update Post - Image Upload

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

Built as a FastAPI backend project demonstrating authentication, database management, REST APIs, authorization, image uploads, search, pagination, email notifications, and API testing.
