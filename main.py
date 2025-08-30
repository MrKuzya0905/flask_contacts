from uuid import uuid4

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from models import db, User, Contact
from config import settings
from forms import SignUpForm, SignInForm, ContactForm

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_uri
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['MAX_FORM_MEMORY_SIZE'] = 1024 * 1024  # 1MB
app.config['MAX_FORM_PARTS'] = 500
db.init_app(app)
csrf_protect = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_message = "Please log in to access this page."
login_manager.login_view = 'sign_in'
login_manager.init_app(app)


# with app.app_context():
#     db.drop_all()
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first_or_404()

@app.route('/signUp/', methods=['GET', 'POST'])
def sign_up():
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
        return redirect(url_for('sign_in'))
    
    return render_template('sign_up.html', form=form)

@app.route('/signIn/', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if not form.validate_on_submit():
        return render_template('sign_in.html', form=form)
    
    user: User = User.query.filter_by(username=form.username.data).first()
    if not user or not user.is_verify_password(pwd=form.password.data):
        flash('Invalid username or password.')
        return redirect(url_for('sign_in'))
    
    login_user(user)
    return redirect(url_for('cabinet'))

@app.get('/')
@login_required
def cabinet():
    return render_template('cabinet.html')

@app.get('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sign_in'))

@app.route('/contact/', methods=['GET', 'POST'])
@login_required
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and secure_filename(file.filename):
            file_name = secure_filename(file.filename)
            file_path = f'static/img/{uuid4().hex}_{file_name}'
            file.save(file_path)
        else:
            file_path = None
        
        contact = Contact(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phobe_number.data,
            city=form.city.data,
            bio=form.bio.data,
            img=file_path,
            user_id=current_user.id
        )
        
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('cabinet'))
    
    return render_template('add_contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)