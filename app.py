from flask import Flask, request, render_template, session, redirect, url_for, flash
from util.accounts import get_salt

app = Flask(__name__)
app.secret_key = get_salt()

users = { "username" : "password" }

@app.route('/')
def index():
    if "username" not in session.keys():
        return redirect(url_for("login"))
    return render_template("index.html")

'''
@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/edit')
def edit():
    return render_tempalte('edit.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
'''

@app.route('/auth', methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.form.get("username") not in users.keys():
        flash("Error: username does not exist")
        return render_template("login.html")
    elif users[request.form.get("username")] != request.form.get("password"):
        flash("Error: password is incorrect") 
        return render_template("login.html")
    elif users[request.form.get("username")] == request.form.get("password"):
        session["username"] = request.form.get("username")
        return redirect(url_for("index"))
    return render_template("login.html")


if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()

