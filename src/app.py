__author__ = 'chansen'

from flask import Flask

app = Flask(__name__)


@app.route('/')                     # https://www.mysite.com/api/
def hello_method():
    return "<h1>sup, dawg!</h1>"


if __name__ == '__main__':
    app.run()
