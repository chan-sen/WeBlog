from src.common.database import Database
from src.models.user import User

__author__ = 'chansen'

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'ggg'


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')                     # https://www.mysite.com/api/
def login_template():
    return render_template('login.html')


@app.route('/register')                     # https://www.mysite.com/api/
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    # authorize login after HTML form submission
    #   render user profile
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        return render_template("profile.html", email=session['email'])
    else:
        return register_template()


@app.route('/auth/register', methods=['POST'])
def register_new_user():
    # authorize register after HTML form submission
    #   render user profile
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    return render_template("profile.html", email=session['email'])


"""
@app.route('/profile', methods=['GET'])
def user_profile():
    # get and render user profile
    user = User.get_by_email(email=session['email'])

    blogs = user.get_blogs()

    return render_template("user_profile.html",
                           email=session['email'],
                           blogs=blogs
                           )
"""

if __name__ == '__main__':
    app.run()
