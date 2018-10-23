from flask import Flask, request, render_template, session, redirect, flash
import util.accounts
import util.posts
import base64

app = Flask(__name__)
app.secret_key = util.accounts.get_salt()


@app.route('/')
def index():
    if util.accounts.is_logged_in(session):
        return render_template(
                    'index_user.html',
                    user=util.accounts.get_logged_in_user(session)
                )
    else:
        return render_template('index_anon.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return redirect('/')
        else:
            return render_template('login.html')

    # Get values passed via POST
    username = request.form.get('username')
    password = request.form.get('password')

    if util.accounts.auth_user(username, password):
        util.accounts.login_user(session, username)
        return redirect('/')
    else:
        flash('Bad username or password')
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return redirect('/')
        else:
            return render_template('signup.html')

    # Get values passed via POST
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if util.accounts.user_exists(username):
        flash('Username already taken')
        return render_template('signup.html')
    elif password != confirm:
        flash('Passwords do not match')
        return render_template('signup.html')
    else:
        util.accounts.add_user(username, password)
        util.accounts.login_user(session, username)
        return redirect('/')


@app.route('/logout')
def logout():
    util.accounts.logout_user(session)
    return redirect('/')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return render_template('create.html')
        else:
            return redirect('/login')

    # Get values passed via POST
    post = util.posts.get_post_id()
    title = request.form.get('title')
    content = request.form.get('content')
    author = util.accounts.get_logged_in_user(session)

    util.posts.create_post(post, title, content, author)
    return redirect('/post?p={post}'.format(post=post))


@app.route('/post')
def post():
    # Get values passed via GET
    post = request.args.get('p')
    content = util.posts.get_post(post)
    title = util.posts.get_title(post)
    #  print(content)
    #  print(content)
    content = util.posts.render_post(content)
    title = util.posts.render_post(title)
    return render_template(
            'post.html',
            title=title,
            content=content
    )


if __name__ == '__main__':
    util.posts.create_table()
    util.accounts.create_table()
    app.debug = True  # Set to `False` before release
    app.run()

