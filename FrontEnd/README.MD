# 🎉 EventPro Nepal - Event Management System

A modern, full-featured web application built with Flask for managing and discovering events in Nepal. This platform enables users to create, browse, register for events, and manage their event participation through an intuitive dashboard with a beautiful, responsive design.

## 🌐 Live Demo
Visit the repository: [Event-Management-System](https://github.com/akashbhatta/Event-Management-System/tree/main/FrontEnd)

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Routes](#-routes)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/akashbhatta/Event-Management-System.git

# Navigate to FrontEnd directory
cd Event-Management-System/FrontEnd

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser at http://127.0.0.1:5000
```

## ✨ Features

### 🎯 Core Functionality
- **User Authentication System**: Secure registration and login with password hashing
- **Event Discovery Platform**: Browse all public events with advanced filtering
- **Event Registration**: One-click registration for events with attendance tracking
- **Personal Dashboard**: Comprehensive event management interface
- **Event Creation & Management**: Full CRUD operations for events
- **Real-time Updates**: Dynamic content loading and updates
- **Responsive Design**: Seamless experience across all devices

### 👤 User Features
- **User Authentication**: Secure registration and login system with password hashing
- **Event Discovery**: Browse all public events with category filtering
- **Event Details**: View comprehensive event information including date, location, and description
- **Event Registration**: Register for events and track participation
- **Personal Dashboard**: Manage created events and view registered events
- **Event Creation**: Create new events with detailed information and images
- **Event Management**: Update or delete your own events
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

### Admin Features
- Pre-seeded admin account for initial content
- Admin events are visible to all users
- Users only see their own created events plus admin events

### Categories
- Tech
- Music
- Sports
- Food
- Travel
- Business
- Health
- Gaming
- Art
- Cultural
- General

## 🛠 Tech Stack

### Backend
- **Framework**: Flask 3.1.2
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Password Security**: Werkzeug password hashing

### Frontend
- **UI Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.0.0
- **Fonts**: Google Fonts (Poppins)
- **Styling**: Custom CSS with modern design patterns

### Additional Libraries
- PyJWT for token handling
- email-validator for email validation
- python-dotenv for environment variables
- Gunicorn for production deployment

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Web browser (Chrome, Firefox, Safari, or Edge)

### Step-by-Step Installation

1. **Clone the repository from GitHub**
   ```bash
   git clone https://github.com/akashbhatta/Event-Management-System.git
   cd Event-Management-System
   ```

2. **Navigate to the FrontEnd directory**
   ```bash
   cd FrontEnd
   ```

3. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database** (automatic on first run)
   The application will automatically create the SQLite database and seed initial data when you first run it.

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 🚀 Usage

### For Regular Users

1. **Registration**
   - Click "Sign Up" in the navigation bar
   - Fill in username, email, and password
   - Submit to create your account

2. **Login**
   - Click "Login" in the navigation bar
   - Enter your email and password
   - Access your personal dashboard

3. **Browse Events**
   - Visit the "Explore" page to see all available events
   - Filter events by category using the dropdown
   - Click on any event to view full details

4. **Register for Events**
   - View event details
   - Click "Register for Event" button
   - Track registered events in your dashboard

5. **Create Events**
   - Login to your account
   - Navigate to "Dashboard"
   - Click "Create New Event"
   - Fill in event details:
     - Title
     - Location
     - Date and Time (format: YYYY-MM-DDTHH:MM)
     - Category
     - Image URL
     - Description
   - Submit to publish your event

6. **Manage Your Events**
   - Go to your Dashboard
   - View "My Events" section
   - Edit or delete your events as needed

### Default Admin Account

The system comes with a pre-seeded admin account:
- **Username**: Nepal_Admin
- **Email**: admin@test.com
- **Password**: password123

**⚠️ Security Note**: Change the admin password immediately after first login in production environments.

### Pre-Seeded Events

The application comes with 12 sample events for 2026 showcasing various categories:
- **Tech Expo KTM** (Tech) - January 20, Kathmandu
- **Lakeside Music** (Music) - February 14, Pokhara
- **Cricket Finals** (Sports) - March 10, Kirtipur
- **Newari Food Day** (Food) - April 5, Bhaktapur
- **Everest Talk** (Travel) - May 29, Namche
- **Startup Night** (Business) - June 12, Thamel
- **Yoga Retreat** (Health) - July 20, Nagarkot
- **Gaming Cup** (Gaming) - August 15, Lalitpur
- **KTM Marathon** (Sports) - September 25, City Center
- **Art Exhibition** (Art) - October 10, Patan
- **Digital Nepal** (Tech) - November 5, Online
- **Peace Fest** (Cultural) - December 30, Lumbini

These events are automatically created on first run to demonstrate the system's capabilities.

## 📁 Project Structure

```
Event-Management-System/
│
├── FrontEnd/
│   ├── instance/
│   │   └── site.db                 # SQLite database (auto-generated)
│   │
│   ├── static/
│   │   ├── CSS/
│   │   │   └── style.css          # Custom styles
│   │   └── JS/
│   │       └── main.js            # Client-side JavaScript
│   │
│   ├── templates/
│   │   ├── base.html              # Base template with navbar/footer
│   │   ├── index.html             # Homepage with featured events
│   │   ├── events.html            # Event listing page
│   │   ├── event_details.html     # Single event view
│   │   ├── dashboard.html         # User dashboard
│   │   ├── create-event.html      # Event creation/editing form
│   │   ├── login.html             # Login page
│   │   ├── register.html          # Registration page
│   │   ├── about.html             # About page
│   │   ├── contact.html           # Contact page
│   │   └── profile.html           # User profile
│   │
│   ├── app.py                     # Main Flask application
│   ├── requirements.txt           # Python dependencies
│   └── README.MD                  # Documentation
│
├── .git/                          # Git repository
└── README.md                      # This file
```

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file in the FrontEnd directory for custom configuration:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development  # Change to 'production' for deployment
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URI=sqlite:///site.db

# Application Settings
DEBUG=True
PORT=5000
```

### Application Configuration (app.py)

```python
# Security
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this!

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session
app.config['SESSION_TYPE'] = 'filesystem'
```

### Updating Secret Key

For security, generate a new secret key:

```python
import secrets
print(secrets.token_hex(16))
```

Copy the output and update `SECRET_KEY` in `app.py`.

## 🗄 Database Schema

### User Model
```python
- id (Integer, Primary Key)
- username (String, Unique, Required)
- email (String, Unique, Required)
- password (String, Hashed, Required)
- events_created (Relationship to Event)
- events_joined (Many-to-Many with Event)
```

### Event Model
```python
- id (Integer, Primary Key)
- title (String, Required)
- location (String, Required)
- date (DateTime, Required)
- description (Text, Required)
- category (String, Default: 'General')
- image_url (String)
- user_id (Foreign Key to User, Required)
- author (Relationship to User)
- attendees (Many-to-Many with User)
```

### Registrations Table (Association Table)
```python
- user_id (Foreign Key to User)
- event_id (Foreign Key to Event)
```

## 🛣 API Routes

### Public Routes
- `GET /` or `/index` - Homepage with featured events
- `GET /events` - All events with category filtering
- `GET /event/<event_id>` - Event details page
- `GET /about` - About page
- `GET /contact` - Contact page
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration

### Protected Routes (Login Required)
- `GET /dashboard` - User dashboard
- `GET /create-event` - Event creation form
- `POST /create-event` - Submit new event
- `GET /event/<event_id>/update` - Edit event form
- `POST /event/<event_id>/update` - Update event
- `POST /event/<event_id>/delete` - Delete event
- `POST /event/<event_id>/register` - Register for event
- `GET /logout` - Logout user

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's security functions
- **Login Protection**: Sensitive routes are protected with `@login_required` decorator
- **CSRF Protection**: Forms are protected with Flask-WTF CSRF tokens
- **Session Management**: Secure user session handling with Flask-Login
- **Input Validation**: Form validation using WTForms validators
- **Privacy Controls**: Users can only edit/delete their own events

## 🚀 Deployment

### Local Development
```bash
# Development mode with auto-reload
python app.py
```
The app runs in debug mode on `http://127.0.0.1:5000`

### Production Deployment

#### Using Gunicorn (Recommended)

1. **Install Gunicorn** (already in requirements.txt)
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

#### Using Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t eventpro-nepal .
docker run -p 5000:5000 eventpro-nepal
```

### Platform-Specific Deployment

#### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Deploy
heroku create your-app-name
git push heroku main
```

#### Railway / Render
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn app:app`

#### PythonAnywhere
1. Upload files to your account
2. Set up virtual environment
3. Configure WSGI file
4. Set static files mapping

**⚠️ Important Production Steps:**
1. **Change SECRET_KEY** to a secure random value
2. **Update admin password** immediately after first deployment
3. **Use PostgreSQL or MySQL** instead of SQLite for production
4. **Set `debug=False`** in app configuration
5. **Use environment variables** for sensitive configurations
6. **Set up proper logging** for monitoring
7. **Use HTTPS** with SSL certificates
8. **Configure CORS** if needed for API access
9. **Set up database backups**
10. **Implement rate limiting** to prevent abuse

## 🐛 Known Issues

- Date input requires specific format (YYYY-MM-DDTHH:MM)
- Image URLs must be provided manually (no file upload yet)
- SQLite is used (not ideal for heavy production use)

## ❓ Troubleshooting & FAQ

### Common Issues

**Q: Application won't start**
```bash
# Check if port 5000 is already in use
lsof -i :5000  # On Unix/Mac
netstat -ano | findstr :5000  # On Windows

# Use a different port
python app.py --port 8000
```

**Q: Database errors on first run**
```bash
# Delete the existing database and restart
rm instance/site.db
python app.py
```

**Q: Module not found errors**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # Unix/Mac
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Q: Can't login with admin credentials**
- Username: `Nepal_Admin`
- Email: `admin@test.com`
- Password: `password123`

If it doesn't work, delete the database and restart the application.

**Q: How to reset the database?**
```bash
# Stop the application
# Delete the database file
rm instance/site.db
# Restart the application - it will recreate with seed data
python app.py
```

## 🔄 Future Enhancements

- [ ] Image upload functionality
- [ ] Email notifications for event reminders
- [ ] Event search functionality
- [ ] User profile customization
- [ ] Event comments and ratings
- [ ] Calendar view for events
- [ ] Export events to calendar apps
- [ ] Social media sharing
- [ ] Payment integration for paid events
- [ ] Event capacity management
- [ ] QR code generation for event tickets
- [ ] Mobile app development

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the repository**
   - Click the 'Fork' button at the top right of the GitHub page

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Event-Management-System.git
   cd Event-Management-System
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

4. **Make your changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines for Python
   - Test your changes thoroughly

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/AmazingFeature
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click 'New Pull Request'
   - Select your fork and branch
   - Describe your changes in detail

### Contribution Guidelines

- **Code Quality**: Ensure your code is clean and well-documented
- **Testing**: Test all features before submitting
- **Commit Messages**: Use clear, descriptive commit messages
- **Documentation**: Update README if you add new features
- **Issues**: Check existing issues before creating new ones
- **Respect**: Be respectful and constructive in discussions

### Development Setup for Contributors

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pylint black

# Run tests (if available)
pytest

# Format code
black .

# Lint code
pylint app.py
```

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Feature Requests

We love new ideas! Submit feature requests as issues with:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach (if you have ideas)

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions professional and on-topic

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors & Contributors

### Main Developer
- **Akash Bhatta** - *Initial work and maintenance*
  - GitHub: [@akashbhatta](https://github.com/akashbhatta)
  - Repository: [Event-Management-System](https://github.com/akashbhatta/Event-Management-System)

### Contributors
Want to see your name here? Check out our [Contributing Guidelines](#-contributing) and submit a pull request!

## 📧 Contact & Support

### Get Help
- **Issues**: [GitHub Issues](https://github.com/akashbhatta/Event-Management-System/issues)
- **Discussions**: [GitHub Discussions](https://github.com/akashbhatta/Event-Management-System/discussions)
- **Email**: admin@test.com

### Social & Resources
- **Repository**: [github.com/akashbhatta/Event-Management-System](https://github.com/akashbhatta/Event-Management-System)
- **Report Bugs**: [Create an Issue](https://github.com/akashbhatta/Event-Management-System/issues/new)
- **Request Features**: [Feature Request](https://github.com/akashbhatta/Event-Management-System/issues/new?labels=enhancement)

### Stay Updated
- ⭐ Star the repository to show support
- 👀 Watch for updates and new releases
- 🍴 Fork to create your own version

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)

## 🙏 Acknowledgments

Special thanks to:
- **Bootstrap Team** - Excellent UI framework
- **Flask Community** - Comprehensive documentation and support
- **Font Awesome** - Beautiful icon library
- **Unsplash** - High-quality placeholder images
- **All Contributors** - Code contributions and testing
- **Open Source Community** - Inspiration and best practices

## 📜 Changelog

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ User authentication system
- ✅ Event CRUD operations
- ✅ Event registration functionality
- ✅ User dashboard
- ✅ Responsive design
- ✅ Pre-seeded database with sample events
- ✅ Category-based event filtering
- ✅ Admin event system

### Planned Updates
See [Future Enhancements](#-future-enhancements) for upcoming features.

## 🗺️ Roadmap

### Phase 1 (Completed) ✅
- [x] Basic authentication system
- [x] Event CRUD operations
- [x] User dashboard
- [x] Responsive design
- [x] Database seeding

### Phase 2 (In Progress) 🚧
- [ ] Image upload functionality
- [ ] Email notifications
- [ ] Enhanced search features
- [ ] User profiles with avatars
- [ ] Event comments and ratings

### Phase 3 (Planned) 📋
- [ ] Payment integration
- [ ] QR code ticketing
- [ ] Calendar integration
- [ ] Social media sharing
- [ ] Mobile application

### Phase 4 (Future) 🌟
- [ ] AI-powered event recommendations
- [ ] Live event streaming
- [ ] Virtual event support
- [ ] Advanced analytics
- [ ] Multi-language support

## 🎯 Project Goals

- Provide a simple, intuitive event management platform
- Support event organizers in Nepal and beyond
- Foster community engagement through events
- Offer a learning resource for Flask developers
- Maintain clean, well-documented code

---

<div align="center">

**Made with ❤️ in Nepal**

[⬆ Back to Top](#-eventpro-nepal---event-management-system)

</div>