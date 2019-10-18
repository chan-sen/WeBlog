from src.common.database import Database
from src.models.user import User

__author__ = 'chansen'

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'ggg'


@app.route('/')                     # https://www.mysite.com/api/
def hello_method():
    return render_template('login.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        return render_template("profile.html", email=session['email'])
    return hello_method()


@app.route('/profile', methods=['GET'])
def user_profile():
    user = User.get_by_email(email=session['email'])

    blogs = user.get_blogs()

    return render_template("user_profile.html",
                           email=session['email'],
                           blogs=blogs,
                           )




if __name__ == '__main__':
    app.run()
