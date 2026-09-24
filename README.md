# Blog Management API — Complete Project Update

## 1. Project Setup

* FastAPI backend created
* SQLite database configured
* Project structure organized into models, schemas, routes, services, and utilities
* Swagger API documentation available

## 2. Authentication

* User registration and login completed
* Password hashing using bcrypt
* JWT authentication implemented
* Protected APIs tested through Swagger

## 3. Blog Posts

* Create posts
* View posts
* Update posts
* Delete posts
* View user's own posts
* Post ownership validation implemented
* Image support implemented

## 4. Comments

* Add comments to posts
* View comments
* Comment validation implemented
* Email notification sent to the post owner when a comment is added

## 5. Likes

* Like posts
* Unlike posts
* Duplicate like prevention
* Email notification sent to the post owner when a post is liked

## 6. Subscription System

Three subscription plans are implemented:

* Basic — ₹99
* Premium — ₹199
* Pro — ₹299

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

### Subscription API Endpoints

| Method | Endpoint                                              | Description                      |
| ------ | ----------------------------------------------------- | -------------------------------- |
| GET    | `/subscriptions/plans`                                | Get available subscription plans |
| POST   | `/subscriptions/`                                     | Create a subscription            |
| POST   | `/subscriptions/renew`                                | Renew an active subscription     |
| GET    | `/subscriptions/me`                                   | Get current user's subscription  |
| GET    | `/subscriptions/billing-history`                      | Get billing history              |
| GET    | `/subscriptions/billing-history/{billing_id}/invoice` | Generate/view invoice            |

## 7. Email Notification System

* SMTP email configuration implemented
* Comment notifications
* Like notifications
* Email testing completed successfully

## 8. Dashboard & Analytics

User dashboard implemented with JWT authentication.

### Dashboard Statistics

* Total posts
* Comments made
* Likes received
* Total post views

### Analytics Charts

Interactive charts implemented using Chart.js:

* Likes per post
* Comments per post

Each user only receives analytics related to their own posts.

## 9. Post View Tracking

* `views` field added to the Post model
* Post views are tracked
* Each post view increments the view count
* Total views displayed on the dashboard

## 10. Dashboard UI

* Responsive dashboard created
* Dark-mode interface
* Statistics cards
* Interactive Chart.js graphs
* JWT-based API data loading
* Mobile-responsive layout
* Access Token management interface
* Toast notifications
* Responsive dashboard components

## 11. Django Admin

* Django admin project integrated
* Subscription plans can be managed through the admin interface
* Billing information can be managed through the admin interface

## 12. 🔔 Notification Center

The project includes an in-app Notification Center with a bell icon for displaying user-specific notifications.

### Notification Features

* Like notifications when another user likes your post
* Comment notifications when another user comments on your post
* Subscription activation notifications
* Subscription renewal notifications
* Unread notification count
* Read/unread notification status
* Mark individual notifications as read
* Mark individual notifications as unread
* Mark all notifications as read
* Responsive notification dropdown
* JWT-protected notification APIs

### Notification API Endpoints

| Method | Endpoint                                  | Description                      |
| ------ | ----------------------------------------- | -------------------------------- |
| GET    | `/notifications/`                         | Get current user's notifications |
| GET    | `/notifications/unread-count`             | Get unread notification count    |
| PUT    | `/notifications/{notification_id}/read`   | Mark notification as read        |
| PUT    | `/notifications/{notification_id}/unread` | Mark notification as unread      |
| PUT    | `/notifications/read-all`                 | Mark all notifications as read   |

### Notification Types

* `like`
* `comment`
* `subscription`

### Notification Testing

The Notification Center was tested successfully through the dashboard and API endpoints.

The following were verified:

* Notification bell
* Notification dropdown
* Like notifications
* Comment notifications
* Subscription notifications
* Unread notification count
* Mark as read
* Mark as unread
* Mark all as read

## 13. 🤖 AI Support Chat

The project includes an AI Support Chat feature that provides instant assistance to authenticated users through a floating support widget in the dashboard.

### AI Support Features

* Floating AI Support chat widget
* Clean and responsive chat interface
* User message input
* Instant AI response display
* Scrollable conversation history
* Persistent chat history
* User-specific chat history
* JWT-protected AI Support APIs
* Chat activity stored in the database
* Responsive dashboard integration

### Supported Topics

The AI Support assistant provides predefined responses for:

* Creating posts
* Editing posts
* Deleting posts
* Subscription management
* Billing and payment information
* Profile management
* Dashboard analytics
* General platform FAQs

### AI Support API Endpoints

| Method | Endpoint           | Description                                        |
| ------ | ------------------ | -------------------------------------------------- |
| GET    | `/api/ai-support/` | Get current user's AI support chat history         |
| POST   | `/api/ai-support/` | Send a question and receive an AI support response |

### AI Support Database Tracking

Each AI support conversation stores:

* User ID
* User question
* AI response
* Created timestamp

### AI Response System

The current implementation uses predefined FAQ-based responses to provide instant assistance without requiring an external AI service.

The backend receives the user's question, processes it through the FAQ response system, returns the appropriate response, and stores the conversation in the database.

### AI Support Testing

The following questions were tested successfully:

* How do I create a post?
* How do I edit my post?
* How do I delete my post?
* How does subscription work?
* How can I check my billing?
* How do I manage my profile?
* What does the dashboard analytics show?
* General platform questions

The AI Support Chat was tested successfully through:

* Swagger API
* Dashboard chat interface
* Chat history loading
* Multiple user questions
* Page refresh and persistent history

## 14. Testing

The following project features were tested successfully:

### Authentication

* User registration
* User login
* JWT authentication
* Protected APIs

### Blog Features

* Post creation
* Post retrieval
* Post update
* Post deletion
* Post ownership validation
* Image support

### Comments & Likes

* Comment creation
* Comment retrieval
* Comment validation
* Like functionality
* Unlike functionality
* Duplicate-like prevention

### Notifications

* Email notifications
* In-app Notification Center
* Like notifications
* Comment notifications
* Subscription notifications
* Read/unread functionality
* Mark all as read

### Subscriptions & Billing

* Subscription plans
* Subscription creation
* Active subscription validation
* Subscription renewal
* Subscription expiry
* Billing history
* Invoice generation

### Dashboard

* Dashboard statistics
* Likes analytics
* Comments analytics
* Post view tracking
* JWT-based dashboard access
* Responsive dashboard UI

### AI Support

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

## 15. GitHub

Project source code has been committed and pushed to GitHub.

Repository:

`https://github.com/Pradeeshs14/Blog_Management.git`
