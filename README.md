## 📌**Overview:**
My Digital Diary is a full-stack web application that enables users to securely create, manage, and organize their personal diary entries online. The platform eliminates the risk of losing traditional handwritten notes while providing advanced digital features for better productivity. Integrated AI-powered chat and text summarization using the Sarvam AI API, implemented a Cloudinary-backed image gallery, and developed a REST API for programmatic access to the to-do list.

## ✨ **Features:**
1. **Task Specific Modules:-** Dedicated sections for Journal, Notes, Ideas, Quotes, To-Do List, and Gallery to keep everything organized in one place.
2. User Authentication:- Secure registration and login using Flask-Login. Passwords are hashed and all routes are protected with session-based authentication and CSRF protection.
3. AI Assistance:- A floating AI chat assistant available on every page, plus one-click summarization for Journal and Notes entries — by using Sarvam AI API.
4. Image Uploads:- Upload and attach images to Notes and Gallery folders. Images are stored persistently on Cloudinary so they never disappear on server restarts.
5. REST API:- A fully functional CRUD REST API for the To-Do list. Includes a built-in live API tester at `/api_docs` so you can test all endpoints directly from the browser without using any external tools.
6. Contact:- A contact form that delivers messages directly to the owner's inbox via Gmail SMTP using Flask-Mail.
7. Full CRUD:- Every module supports creating, reading, updating, and deleting entries with changes reflected in the database instantly.
   
## 🛠️ **Tech Stack:**
1. Backend:- Python, Flask
2. Database:- MySQL (hosted on Aiven Cloud)
3. ORM:- SQLAlchemy + Flask-Migrate (Alembic)
4. Auth:- Flask-Login
5. Frontend:- HTML, CSS, Jinja2, Bootstrap
6. Image Storage :- Cloudinary
7. API:- Sarvam AI API
8. Deployment:- Render

## 🧠 **Architecture:**
1. Used Flask Blueprints for modular structure.
2. Flask-Login for session-based authentication
3. Uses SQLAlchemy ORM for database management.
4. External API integration for AI feature.
5. Cloudinary for persistent image storage.
6. REST API layer **(`/api/`)** for the To-Do feature — returns JSON, supports GET, POST, PATCH, DELETE.

## 🚀 **Live Demo:**
https://my-digital-diary.onrender.com/

## REST API base URL (needs login)
https://my-digital-diary.onrender.com/api_docs

## 📸 **Screenshots:**
### 🏠 Login Page
![Login](screenshots/Login.png)

### 📝 Journal Feature
![Journal](screenshots/Journal.png)

### 🤖 AI Assistance Feature
![AI](screenshots/AI.png)

### { } API Docs Page
![AI](screenshots/API.png)

## 🤝 **Contributing:**
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## 📬 **Contact:**
Krishnathombare43@gmail.com

⭐**~ If you found this project useful, consider starring the repository!**
