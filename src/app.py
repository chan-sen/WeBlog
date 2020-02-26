from common.database import Database
from models.blog import Blog
from models.user import User

__author__ = 'chansen'

from flask import (Flask,
                   render_template, request, session,
                   redirect, url_for, make_response)

app = Flask(__name__)
app.secret_key = 'ggg'


@app.route('/')
def home_template():
    if 'email' not in session or session['email'] is None:
        return render_template('home.html')
    else:
        return redirect(url_for('user_profile'))


@app.route('/login')                    # https://www.mysite.com/api/
def login_template():
    if 'email' not in session or session['email'] is None:
        return render_template('login.html')
    else:
        return redirect(url_for('user_profile'))


@app.route('/register')                 # https://www.mysite.com/api/
def register_template():
    if 'email' not in session or session['email'] is None:
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
        return redirect(url_for('user_blogs'))
    else:
        return redirect(url_for('register_template'))


@app.route('/blogs')
@app.route('/<string:username>/blogs')
def user_blogs(username=None):
    if username is not None:
        user = User.get_by_username(username)
    elif 'email' not in session or session['email'] is None:
        return redirect(url_for('login_template'))
    else:
        return redirect(url_for('user_profile'))
    blogs = user.get_blogs()
    return render_template("user_blogs.html", email=user.email, blogs=blogs)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if session['email']:
        if request.method == 'GET':
            return render_template('new_blog.html')
        else:
            title = request.form['title']
            description = request.form['description']
            user = User.get_by_email(session['email'])
            user.new_blog(title, description)

            return redirect(url_for('user_profile'))
    else:
        return redirect(url_for('login_template'))


@app.route('/<string:author>/blog/<string:blog_id>')
def blog_posts(author, blog_id):
    if session['email']:
        user = User.get_by_email(session['email'])
    else:
        user = None
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('blog_page.html',
                           user=user,
                           author=author,
                           posts=posts,
                           blog_id=blog_id,
                           blog_title=blog.title)


@app.route('/<string:author>/blog/<string:blog_id>/post/new', methods=['POST', 'GET'])
def new_post_on_blog(author, blog_id):
    if session['email']:
        if request.method == 'GET':
            return render_template('new_post.html')
        else:
            title = request.form['title']
            content = request.form['content']
            blog = Blog.from_mongo(blog_id)
            blog.new_post(title, content)
            return redirect(url_for('blog_posts',
                                    author=author,
                                    blog_id=blog_id))
    else:
        return redirect(url_for('login_template'))


@app.route('/profile', methods=['GET'])
def user_profile():
    # get and render user profile
    if 'email' in session or session['email'] is not None:
        user = User.get_by_email(email=session['email'])

        blogs = user.get_blogs()

        return render_template("user_profile.html",
                               user=user,
                               email=session['email'],
                               blogs=blogs)
    else:
        return redirect(url_for('login_template'))


if __name__ == '__main__':
    app.run()
