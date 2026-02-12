from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import text
import os

# --- 1. SETUP ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- 2. MODELS ---
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

def allowed_image(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_IMAGE_EXTENSIONS

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    events_created = db.relationship('Event', backref='author', lazy=True)
    registrations = db.relationship('Registration', backref='user', lazy=True, cascade='all, delete-orphan')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')
    image_url = db.Column(db.String(500))
    organizer_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')

    @property
    def attendees(self):
        return [registration.user for registration in self.registrations]

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    short_info = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- 3. FORMS ---
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
    organizer_name = StringField('Organizer Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DDTHH:MM)', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    image_url = StringField('Image URL')
    image_file = FileField('Upload Image')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Event')

class RegistrationForm(FlaskForm):
    short_info = TextAreaField('Short Information', validators=[DataRequired()])
    submit = SubmitField('Submit Registration')

# --- 4. ROUTES ---
def prioritize_events(events):
    now = datetime.utcnow()
    soon_window = now + timedelta(days=7)
    for event in events:
        event.is_expired = event.date < now
        event.is_soon = now <= event.date <= soon_window
        delta = event.date - now
        event.days_left = int(delta.total_seconds() // 86400)
        event.hours_left = int(delta.total_seconds() // 3600)
    def sort_key(event):
        if event.is_soon:
            bucket = 0
        elif not event.is_expired:
            bucket = 1
        else:
            bucket = 2
        ts = event.date.timestamp()
        if event.is_expired:
            ts = -ts
        return (bucket, ts)
    return sorted(events, key=sort_key), now

@app.route("/")
@app.route("/index")
def index():
    admin = User.query.filter_by(username="Nepal_Admin").first()
    admin_id = admin.id if admin else 1
    if current_user.is_authenticated:
        # PRIVACY: Admin Events + MY Events only
        events = Event.query.filter((Event.user_id == admin_id) | (Event.user_id == current_user.id)).order_by(Event.date.asc()).all()
    else:
        events = Event.query.filter_by(user_id=admin_id).order_by(Event.date.asc()).all()
    events, now = prioritize_events(events)
    return render_template('index.html', events=events, now=now)

@app.route("/events")
def events():
    cat = request.args.get('category')
    admin = User.query.filter_by(username="Nepal_Admin").first()
    admin_id = admin.id if admin else 1
    query = Event.query.filter((Event.user_id == admin_id) | (Event.user_id == (current_user.id if current_user.is_authenticated else -1)))
    if cat: query = query.filter_by(category=cat)
    all_events = query.order_by(Event.date.asc()).all()
    all_events, now = prioritize_events(all_events)
    return render_template('events.html', events=all_events, now=now)

@app.route("/dashboard")
@login_required
def dashboard():
    my_events = Event.query.filter_by(author=current_user).all()
    joined_events = [registration.event for registration in current_user.registrations]
    return render_template('dashboard.html', my_events=my_events, joined_events=joined_events)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user); return redirect(url_for('dashboard'))
        flash('Login Failed', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user); db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/create-event", methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        try: date_obj = datetime.strptime(form.date.data, '%Y-%m-%dT%H:%M')
        except: date_obj = datetime.utcnow()
        image_url = form.image_url.data.strip() if form.image_url.data else ''
        image_file = request.files.get('image_file')
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            if allowed_image(filename):
                os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
                save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                image_file.save(save_path)
                image_url = f"/{app.config['UPLOAD_FOLDER'].replace(os.sep, '/')}/{filename}"
        if not image_url:
            image_url = "https://placehold.co/1200x600?text=Event+Image"
        event = Event(title=form.title.data, location=form.location.data, date=date_obj,
                      category=form.category.data, image_url=image_url,
                      organizer_name=form.organizer_name.data,
                      description=form.description.data, author=current_user)
        db.session.add(event); db.session.commit()
        return redirect(url_for('index'))
    if request.method == 'GET' and not form.organizer_name.data:
        form.organizer_name.data = current_user.username
    return render_template('create-event.html', form=form)

@app.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user: return redirect(url_for('index'))
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.organizer_name = form.organizer_name.data
        event.location = form.location.data
        event.description = form.description.data
        event.category = form.category.data
        image_url = form.image_url.data.strip() if form.image_url.data else event.image_url
        image_file = request.files.get('image_file')
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            if allowed_image(filename):
                os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
                save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                image_file.save(save_path)
                image_url = f"/{app.config['UPLOAD_FOLDER'].replace(os.sep, '/')}/{filename}"
        event.image_url = image_url
        db.session.commit(); return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.organizer_name.data = event.organizer_name or event.author.username
        form.location.data = event.location
        form.description.data = event.description
        form.category.data = event.category
        form.image_url.data = event.image_url
        form.date.data = event.date.strftime('%Y-%m-%dT%H:%M')
    return render_template('create-event.html', form=form, title="Update Event")

@app.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author == current_user:
        db.session.delete(event); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/event/<int:event_id>")
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    reg_form = RegistrationForm()
    is_registered = False
    if current_user.is_authenticated:
        is_registered = any(registration.user_id == current_user.id for registration in event.registrations)
    return render_template('event_details.html', event=event, reg_form=reg_form, is_registered=is_registered)

@app.route("/event/<int:event_id>/register", methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = RegistrationForm()
    if not form.validate_on_submit():
        flash('Please add a short introduction before registering.', 'warning')
        return redirect(url_for('event_details', event_id=event.id))
    existing = Registration.query.filter_by(user_id=current_user.id, event_id=event.id).first()
    if not existing:
        registration = Registration(user_id=current_user.id, event_id=event.id, short_info=form.short_info.data)
        db.session.add(registration); db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/event/<int:event_id>/registrations")
@login_required
def event_registrations(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        return redirect(url_for('dashboard'))
    registrations = Registration.query.filter_by(event_id=event.id).order_by(Registration.created_at.desc()).all()
    return render_template('event_registrations.html', event=event, registrations=registrations)

@app.route("/logout")
def logout(): logout_user(); return redirect(url_for('index'))
@app.route("/about")
def about(): return render_template('about.html')
@app.route("/contact")
def contact(): return render_template('contact.html')

# --- 5. INITIALIZATION & SEEDER ---
def seed_database():
    admin = User.query.filter_by(username="Nepal_Admin").first()
    if not admin:
        admin = User(username="Nepal_Admin", email="admin@test.com", password=generate_password_hash("password123"))
        db.session.add(admin); db.session.commit()
    if Event.query.count() > 5: return # Skip if already seeded
    
    events_2026 = [
        {"title": "Tech Expo KTM", "cat": "Tech", "loc": "Kathmandu", "date": datetime(2026, 1, 20), "img": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800"},

        {"title": "Lakeside Music", "cat": "Music", "loc": "Pokhara", "date": datetime(2026, 2, 14), "img": "https://superdesk-pro-c.s3.amazonaws.com/sd-nepalitimes/2022111015118/636d05f09c7e80680e0a5f36jpeg.jpg"},

        {"title": "Cricket Finals", "cat": "Sports", "loc": "Kirtipur", "date": datetime(2026, 3, 10), "img": "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800"},

        {"title": "Newari Food Day", "cat": "Food", "loc": "Bhaktapur", "date": datetime(2026, 4, 5), "img": "https://fis-api.kathmanducookingacademy.com/media/attachments/Newari%20dish.jpg"},

        {"title": "Everest Talk", "cat": "Travel", "loc": "Namche", "date": datetime(2026, 5, 29), "img": "https://api.luxuryholidaynepal.com/media/trip-gallery/media-a68cf26f-1751444735.jpg"},

        {"title": "Startup Night", "cat": "Business", "loc": "Thamel", "date": datetime(2026, 6, 12), "img": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800"},

        {"title": "Yoga Retreat", "cat": "Health", "loc": "Nagarkot", "date": datetime(2026, 7, 20), "img": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800"},

        {"title": "Gaming Cup", "cat": "Gaming", "loc": "Lalitpur", "date": datetime(2026, 8, 15), "img": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800"},

        {"title": "KTM Marathon", "cat": "Sports", "loc": "City Center", "date": datetime(2026, 9, 25), "img": "https://images.contentstack.io/v3/assets/bltd427b71c2e191abd/blta093fe235e5a32ab/67ee0ed3221e860e3f6f7623/Blog-marathon-running-gear-checklist-1600x700.jpg?format=webp&quality=80"},

        {"title": "Art Exhibition", "cat": "Art", "loc": "Patan", "date": datetime(2026, 10, 10), "img": "https://images.unsplash.com/photo-1531058020387-3be344556be6?w=800"},

        {"title": "Digital Nepal", "cat": "Tech", "loc": "Online", "date": datetime(2026, 11, 5), "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800"},

        {"title": "Peace Fest", "cat": "Cultural", "loc": "Lumbini", "date": datetime(2026, 12, 30), "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/The_World_Peace_Pagoda_-_Lumbini.jpg/1280px-The_World_Peace_Pagoda_-_Lumbini.jpg"},
    ]
    for e in events_2026:
        db.session.add(Event(title=e["title"], location=e["loc"], date=e["date"], category=e["cat"], image_url=e["img"], author=admin, description="Best event of 2026!"))
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    app.run(debug=True)




