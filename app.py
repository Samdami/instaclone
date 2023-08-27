from flask import Flask, render_template, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin, current_user
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'my_login.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '5e0b18fd5de07e49f80cb4f8'

"""
To get a 12-digit (any number of choice) secret key, run this in the terminal:

python
import secrets
secrets.token_hex(12)
exit()

Copy the token from the terminal and paste it as the secret key in app.config above
"""

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    """This is the User database model"""
    id = db.Column(db.Integer(), primary_key=True)
    # username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
   

    def __repr__(self):
        return f"User <{self.username}>"

# class BlogPost(db.Model):
#     """This is the blogpost database model"""
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(50))
#     subtitle = db.Column(db.String(50))
#     date_posted = db.Column(db.DateTime)
#     content = db.Column(db.Text)
#     author = db.Column(db.Text)
   

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('signup.html')


          


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = User.query.filter_by(username=username).first()

#         if user and check_password_hash(user.password_hash, password):
#             login_user(user)
#             return redirect(url_for('index'))
#         else:
#             return render_template('login.html', error_msg="Invalid username or password. Try again.")
#     return render_template('login.html')


# @app.route('/logout')
# def logout():
#     logout_user() 
#     return redirect(url_for('login'))


# @app.route('/protected')
# @login_required
# def protected():
#     return render_template('protected.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # user = User.query.filter_by(email=email).first()
        # if user:
        #     flash("Email already exists.")
        # elif len(password) < 6:
        #     flash("Password must be at least 6 characters.")    
        # else:
            
     
       

            # return render_template('signup.html', username_error=username_msg, email_error=email_msg)

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()


    return render_template('signup.html')

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)