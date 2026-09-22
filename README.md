# Blog Management API — Complete Project Update

## 1. Project Setup

- FastAPI backend created
- SQLite database configured
- Project structure organized into models, schemas, routes, services, and utilities
- Swagger API documentation available

## 2. Authentication

- User registration and login completed
- Password hashing using bcrypt
- JWT authentication implemented
- Protected APIs tested through Swagger

## 3. Blog Posts

- Create posts
- View posts
- Update posts
- Delete posts
- View user's own posts
- Post ownership validation implemented
- Image support implemented

## 4. Comments

- Add comments to posts
- View comments
- Comment validation implemented
- Email notification sent to the post owner when a comment is added

## 5. Likes

- Like posts
- Unlike posts
- Duplicate like prevention
- Email notification sent to the post owner when a post is liked

## 6. Subscription System

Three subscription plans implemented:

- Basic — ₹99
- Premium — ₹199
- Pro — ₹299

Features include:

- 30-day subscriptions
- Post limits
- Image limits
- Like limits
- Comment limits
- Active subscription validation
- Subscription expiry handling
- Billing history
- Invoice PDF generation

## 7. Email Notification System

- SMTP email configuration implemented
- Comment notifications
- Like notifications
- Email testing completed successfully

## 8. Dashboard & Analytics

User dashboard implemented with JWT authentication.

Dashboard displays:

- Total posts
- Comments made
- Likes received
- Total post views

Analytics charts implemented using Chart.js:

- Likes per post
- Comments per post

Each user only receives analytics for their own posts.

## 9. Post View Tracking

- `views` field added to the Post model
- Each post view increments the view count
- Total views displayed on the dashboard

## 10. Dashboard UI

- Responsive dashboard created
- Dark-mode interface
- Statistics cards
- Interactive Chart.js graphs
- JWT-based API data loading
- Mobile-responsive layout

## 11. Django Admin

- Django admin project integrated
- Subscription plans and billing information can be managed through the admin interface

## 12. Testing

The following features were tested through Swagger/API:

- Registration
- Login
- JWT authentication
- Post CRUD
- Comments
- Likes/unlikes
- Email notifications
- Subscriptions
- Billing history
- Invoice generation
- Subscription expiry
- Dashboard analytics
- Post view tracking

## 13. GitHub

Project source code has been pushed to GitHub.

Repository:
`https://github.com/Pradeeshs14/Blog_Management.git`

## 14. Deliverables

- Functional Blog Management API
- User authentication
- Subscription management
- Email notification system
- Invoice generation
- User dashboard
- Data visualization
- Post view analytics
- Django admin
- Dashboard screenshot
- GitHub repository
