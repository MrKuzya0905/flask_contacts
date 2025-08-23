from uuid import uuid4

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from models import db, User, Contact
from config import settings
from forms import SignUpForm, SignInForm, ContactForm

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_uri
db.init_app(app)

login_manager = LoginManager()
login_manager.login_message = "Please log in to access this page."
login_manager.login_view = 'login'
login_manager.init_app(app)


# with app.app_context():
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first_or_404()

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            full_name=form.full_name.data,
            phone_number=form.phone_number.data
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up!')
        return redirect(url_for('login'))
    
    return render_template('sign_up.html', form=form)

@app.route('/signIn/', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if not form.validate_on_submit():
        return render_template('sign_in.html', form=form)
    
    user: User = User.query.filter_by(username=form.username.data).first()
    if not user or user.is_verify_password(pwd=form.password.data):
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    
    login_user(user)
    return redirect(url_for('cabinet'))

@app.get('/cabinet/')
@login_required
def cabinet():
    return render_template('cabinet.html')

@app.route('/contact/', methods=['GET', 'POST'])
