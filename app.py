from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
def signup();
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True  # Set to `False` before release
    app.run()

