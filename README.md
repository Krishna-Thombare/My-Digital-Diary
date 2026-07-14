## 📌**Overview:**
My Digital Diary is a full-stack web application that enables users to securely create, manage, and organize their personal diary entries online. The platform eliminates the risk of losing traditional handwritten notes while providing advanced digital features for better productivity. Integrated AI-powered chat and text summarization using the Sarvam AI API, implemented a Cloudinary-backed image gallery, and developed a REST API for programmatic access to the to-do list.

## ✨ **Features:**
1. Task Specific Modules :- Journal, Notes, Ideas, Quotes, To-Do List, Gallery, AI Assistance
2. User Authentication :- Secure registration and login using Flask-Login with session management
3. AI Assistance :- AI-powered chat and one-click text summarization via Sarvam AI API
4. Image Storage :- Persistent image uploads for Notes and Gallery via Cloudinary
5. REST API :- Full CRUD REST API for the To-Do list with a built-in live API tester
6. Full CRUD :- Create, read, update, and delete across all feature modules
   
## 🛠️ **Tech Stack:**
1. Backend:- Python, Flask
2. Database:- MySQL (Aiven Cloud)
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
