from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import text 

# 1. SETUP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 2. DATABASE TABLES
registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    events_created = db.relationship('Event', backref='author', lazy=True)
    events_joined = db.relationship('Event', secondary=registrations, backref='attendees')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')
    image_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 3. FORMS
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DDTHH:MM)', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Event')

# 4. ROUTES
@app.route("/")
@app.route("/index")
def index():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('index.html', events=events)

# FIXED: Added the missing 'events' route
@app.route("/events")
def events():
    all_events = Event.query.order_by(Event.date.asc()).all()
    return render_template('events.html', events=all_events)

# FIXED: Added the missing 'about' route
@app.route("/about")
def about():
    return render_template('about.html')

# FIXED: Added the missing 'contact' route
@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login Failed', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    my_events = Event.query.filter_by(author=current_user).all()
    joined_events = current_user.events_joined
    return render_template('dashboard.html', my_events=my_events, joined_events=joined_events)

@app.route("/create-event", methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        try: date_obj = datetime.strptime(form.date.data, '%Y-%m-%dT%H:%M')
        except: date_obj = datetime.utcnow()
        new_event = Event(title=form.title.data, location=form.location.data, 
                          date=date_obj, description=form.description.data, 
                          category="User Hosted", image_url="https://placehold.co/600x400/3498db/FFF?text=Hosted+Event",
                          author=current_user)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create-event.html', form=form)

@app.route("/event/<int:event_id>")
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)

@app.route("/event/<int:event_id>/register", methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event not in current_user.events_joined:
        current_user.events_joined.append(event)
        db.session.commit()
        flash('Registered!', 'success')
    return redirect(url_for('dashboard'))

# --- 5. STARTUP & 2026 SEEDER ---
def seed_database():
    if Event.query.first(): return 
    admin_pw = generate_password_hash("password123")
    admin = User(username="Nepal_Admin", email="admin@test.com", password=admin_pw)
    db.session.add(admin)
    db.session.commit()

    events_2026 = [
        {"title": "Tech Expo KTM", "cat": "Tech", "loc": "Kathmandu", "date": datetime(2026, 1, 20, 10, 0), "img": "https://placehold.co/600x400/1e3c72/FFF?text=Tech+Expo"},
        {"title": "Lakeside Music", "cat": "Music", "loc": "Pokhara", "date": datetime(2026, 2, 14, 18, 0), "img": "https://placehold.co/600x400/e74c3c/FFF?text=Music+Fest"},
        {"title": "Cricket Finals", "cat": "Sports", "loc": "Kirtipur", "date": datetime(2026, 3, 10, 13, 0), "img": "https://placehold.co/600x400/2ecc71/FFF?text=Cricket"},
        {"title": "Newari Food Day", "cat": "Food", "loc": "Bhaktapur", "date": datetime(2026, 4, 5, 12, 0), "img": "https://placehold.co/600x400/f39c12/FFF?text=Food+Day"},
        {"title": "Everest Talk", "cat": "Travel", "loc": "Namche", "date": datetime(2026, 5, 29, 15, 0), "img": "https://placehold.co/600x400/34495e/FFF?text=Everest"},
        {"title": "Startup Night", "cat": "Business", "loc": "Thamel", "date": datetime(2026, 6, 12, 19, 0), "img": "https://placehold.co/600x400/9b59b6/FFF?text=Startup"},
        {"title": "Yoga Retreat", "cat": "Health", "loc": "Nagarkot", "date": datetime(2026, 7, 20, 6, 0), "img": "https://placehold.co/600x400/1abc9c/FFF?text=Yoga"},
        {"title": "Gaming Cup", "cat": "Gaming", "loc": "Lalitpur", "date": datetime(2026, 8, 15, 11, 0), "img": "https://placehold.co/600x400/d35400/FFF?text=Gaming"},
        {"title": "KTM Marathon", "cat": "Sports", "loc": "City Center", "date": datetime(2026, 9, 25, 7, 0), "img": "https://placehold.co/600x400/c0392b/FFF?text=Marathon"},
        {"title": "Art Exhibition", "cat": "Art", "loc": "Patan", "date": datetime(2026, 10, 10, 10, 0), "img": "https://placehold.co/600x400/7f8c8d/FFF?text=Art"},
        {"title": "Digital Nepal", "cat": "Tech", "loc": "Online", "date": datetime(2026, 11, 5, 14, 0), "img": "https://placehold.co/600x400/2980b9/FFF?text=Digital"},
        {"title": "Peace Fest", "cat": "Cultural", "loc": "Lumbini", "date": datetime(2026, 12, 30, 16, 0), "img": "https://placehold.co/600x400/2c3e50/FFF?text=Peace"},
    ]

    for e in events_2026:
        new_event = Event(title=e["title"], location=e["loc"], date=e["date"], 
                          category=e["cat"], image_url=e["img"], author=admin, description="Best event of 2026!")
        db.session.add(new_event)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.execute(text("DROP VIEW IF EXISTS registration_details"))
        db.session.execute(text("CREATE VIEW registration_details AS SELECT user.username AS User_Name, event.title AS Event_Name FROM registrations JOIN user ON registrations.user_id = user.id JOIN event ON registrations.event_id = event.id;"))
        db.session.commit()
        seed_database() 
    app.run(debug=True)
