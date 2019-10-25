from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User

__author__ = 'chansen'

from flask import (Flask,
                   render_template,
                   request, session,
                   redirect, url_for)

app = Flask(__name__)
app.secret_key = 'ggg'


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')                    # https://www.mysite.com/api/
def login_template():
    if session['email'] is None:
        return render_template('login.html')
    else:
        return redirect(url_for('user_profile'))


@app.route('/register')                 # https://www.mysite.com/api/
def register_template():
    if session['email']:
        return render_template('register.html')
    else:
        return redirect(url_for('user_profile'))


@app.route('/logout')
def logout():
    User.logout()
    return redirect(url_for('login_template'))


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    # authorize login after HTML form submission
    #   render user profile
    username = request.form['username']
    password = request.form['password']

    if User.login_valid(username, password):
        User.login(User.get_by_username(username).email)
        return redirect(url_for('user_profile'))
    else:
        return redirect(url_for('login_template'))


@app.route('/auth/register', methods=['POST'])
def register_new_user():
    # authorize register after HTML form submission
    #   render user profile
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if User.register_valid(username, email, password):
        User.login(email)
        print("user logged in")
        return redirect(url_for('user_blogs'))
    else:
        return redirect(url_for('register_template'))


@app.route('/blogs')
@app.route('/blogs/<string:user_id>')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    elif session['email'] is None:
        return redirect(url_for('login_template'))
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template("user_blogs.html", email=user.email, blogs=blogs)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title)


@app.route('/profile', methods=['GET'])
def user_profile():
    # get and render user profile
    user = User.get_by_email(email=session['email'])

    blogs = user.get_blogs()

    return render_template("user_profile.html",
                           user=user,
                           email=session['email'],
                           blogs=blogs)


if __name__ == '__main__':
    app.run()
