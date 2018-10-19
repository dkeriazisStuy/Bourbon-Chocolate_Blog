from flask import Flask, request, render_template, session, redirect, flash
import util.accounts

app = Flask(__name__)
app.secret_key = util.accounts.get_salt()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

#  @app.route('/search')
#  def search():
#  return render_template('search.html')

@app.route('/edit')
def edit():
    if not util.accounts.is_logged_in(session):
        return redirect('/')
    return render_template('edit.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if util.accounts.is_logged_in(session):
            return redirect('/')
        else:
            return render_template("login.html")

    # Get values passed via POST
    username = request.form.get("username")
    password = request.form.get("password")

    if util.accounts.auth_user(username, password):
        util.accounts.login_user(session, username)
        return redirect('/')
    else:
        flash('Bad username or password')
        return render_template('login.html')

#@app.route('/logout')
#def logout():
    
    

if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()

