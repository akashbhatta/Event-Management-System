# Event Management System 🎉

A full-stack web application that simplifies event creation, discovery, and registration.

Built with Flask and Bootstrap, this platform enables organizers to manage events 
efficiently while providing users with an intuitive interface to discover and 
register for events seamlessly. Features include secure authentication, real-time 
registration tracking, admin dashboard, and responsive design.

https://akashbhatta.pythonanywhere.com/

---

## Features

- **User Authentication** - Secure registration and login
- **Event Management** - Create, edit, and delete events
- **Event Registration** - Browse and register for events
- **Admin Panel** - Manage users, events, and registrations
- **Responsive Design** - Works on mobile, tablet, and desktop
- **Search & Filter** - Find events by category, date, or location

---

## Tech Stack

**Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript  
**Backend:** Python, Flask, SQLAlchemy  
**Database:** SQLite (development), PostgreSQL (production)  
**Authentication:** Flask-Login, Werkzeug

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Event-Management-System.git
cd Event-Management-System
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/events.db
FLASK_ENV=development
```

### 5. Initialize database
```bash
flask db upgrade
```

### 6. Create admin user
```bash
python
>>> from app import app, db
>>> from app.models import User
>>> with app.app_context():
...     admin = User(username='admin', email='admin@events.com', role='admin')
...     admin.set_password('Admin@123')
...     db.session.add(admin)
...     db.session.commit()
>>> exit()
```

### 7. Run the application
```bash
python app.py
```

Visit **http://localhost:5000**

---

## Project Structure

```
EVENT-MANAGEMENT-SYSTEM/
│
├── FrontEnd/                        # Main application directory
│   │
│   ├── instance/                    # Instance folder (auto-generated)
│   │   └── events.db               # SQLite database file
│   │
│   ├── static/                      # Static files (CSS, JS, images)
│   │   ├── CSS/
│   │   │   └── style.css           # Custom stylesheet
│   │   ├── JS/
│   │   │   └── main.js             # JavaScript functionality
│   │   └── uploads/                # User-uploaded images
│   │
│   └── templates/                   # HTML templates (Jinja2)
│       ├── base.html               # Base template (layout)
│       ├── index.html              # Homepage
│       ├── events.html             # Events listing page
│       ├── event_details.html      # Event detail page
│       ├── login.html              # Login page
│       ├── register.html           # User registration page
│       ├── dashboard.html          # User dashboard
│       ├── profile.html            # User profile page
│       ├── create-event.html       # Event creation form (Admin)
│       ├── event_registrations.html # Event registrations (Admin)
│       ├── about.html              # About page
│       ├── contact.html            # Contact page
│       └── 404.html                # Error page
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore file
├── .env                            # Environment variables (create this)
└── README.md                       # Project documentation
```

---

## Screenshots

### Homepage
https://github.com/akashbhatta/Event-Management-System/blob/main/Screenshot%202026-02-11%20221059.png?raw=true

### Explore Page
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-11%20221426.png

### Event Details Page
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-11%20221538.png

### Dashboard
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-11%20222241.png

### Login
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-11%20221631.png

### Contact
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-11%20222103.png

### Register
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-11%20221611.png

### Create Events page
https://github.com/akashbhatta/Event-Management-System/blob/68722ecd56512585beda858d1967c7bda04ccc1c/Screenshot%202026-02-14%20134258.png

---

## Database Schema

**User** → (one-to-many) → **Event** ← (many-to-many) → **Registration**

```sql
Users: id, username, email, password, role
Events: id, title, description, date, location, capacity
Registrations: id, user_id, event_id, status
```

---

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Events
- `GET /events` - List all events
- `GET /events/<id>` - Event details
- `POST /events/create` - Create event (Admin)
- `POST /events/<id>/register` - Register for event

### Admin
- `GET /admin/dashboard` - Admin panel
- `GET /admin/users` - Manage users
- `GET /admin/registrations` - View registrations

---

## Deployment

### PythonAnywhere
1. Upload files to PythonAnywhere
2. Set up virtual environment
3. Configure WSGI file
4. Add environment variables
5. Reload web app

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku run flask db upgrade
```

---

## Requirements

```txt
Flask==2.3.0
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
Flask-Migrate==4.0.4
Werkzeug==2.3.0
email-validator==2.0.0
python-dotenv==1.0.0
```

---

## Default Credentials

**Admin Account:**  
Email: `admin@test.com`  
Password: `password123`

⚠️ **Change these credentials after first login!**

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Akash Bhatta**  
BIT Second Year, Texas College of Management & IT  
https://github.com/akashbhatta

---

## Acknowledgments

- **Mr. Ashish Gautam** - Course Instructor (Web Technology - BIT233)
- **Texas College of Management & IT** - Academic Institution
- Flask Documentation
- Bootstrap Team

---

<div align="center">

**Made with ❤️ for Web Technology (BIT233)**

⭐ Star this repo if you found it helpful!

</div>
