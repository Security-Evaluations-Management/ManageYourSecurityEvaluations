from flask import Flask, render_template, escape

server = Flask(__name__)


@server.route('/')
def home_page():  # put application's code here
    return render_template('index.html')


@server.route('/login')
def login():  # put application's code here
    return render_template("login.html")


if __name__ == '__main__':
    server.run()
