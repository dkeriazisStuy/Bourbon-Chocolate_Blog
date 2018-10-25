from flask import Flask, request, render_template, session, redirect, flash
import util.accounts
import util.posts
import base64

app = Flask(__name__)
app.secret_key = util.accounts.get_salt()


@app.route('/')
def index():
    ids = util.posts.get_all_posts()
    post_list = [util.posts.get_formatted_post(post_id) for post_id in ids]
    print(post_list)
    if util.accounts.is_logged_in(session):
        print('Logged in!')
        return render_template(
            'index_user.html',
            posts=post_list,
            logged_in=util.accounts.get_logged_in_user(session)
        )
    else:
        print('Not logged in!')
        return render_template(
            'index_anon.html',
            posts=post_list
        )


@app.route('/blog')
def blog():
    return render_template('blog.html')


#  @app.route('/search')
#  def search():
    #  return render_template('search.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    post = request.args.get('p')
    if not util.accounts.is_logged_in(session):
        return redirect('/')
    if request.method == 'GET':
        title, content, author, _ = util.posts.get_post(post)
        # content = util.posts.render_post(content)
        if util.accounts.get_logged_in_user(session) == author:
            return render_template(
                'edit.html',
                button_name='Edit Post',
                post = post,
                old_post_title=title,
                old_post_content=content,
                author=author
            )
        else:
            print (util.accounts.get_logged_in_user(session) + "\n" + author)
            return redirect('/')

    # Get values passed via POST
    title = request.form.get('post_title')
    content = request.form.get('post_content')
    post = request.form.get('post')

    if title is None:
        title = ''
    if content is None:
        content = ''

    util.posts.edit_post(post,title,content)
    return redirect('/post?p={post}'.format(post=post))


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

    if 'ret_path' in session:
        ret_path = session['ret_path']
        del session['ret_path']
    else:
        ret_path = '/'

    if util.accounts.auth_user(username, password):
        util.accounts.login_user(session, username)
        return redirect(ret_path)
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
        if util.accounts.valid_password(password):
            password_error = ''
        else:
            password_error = 'Please enter a password ' \
                '8 or more characters in length.'

        if util.accounts.valid_username(username):
            username_error = ''
        else:
            username_error = \
                'Username must be between 1 - 32 characters. ' \
                'Only letters, numbers, ' \
                'hyphens (-), and underscores (_) are allowed.'

        account_created = util.accounts.add_user(username, password)
        if not account_created:  # Account not created properly
            return render_template(
                'signup.html',
                password_error=password_error,
                username_error=username_error
            )
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
            return render_template(
                'create_v1.html',
                button_name='Create Post'
            )
        else:
            # Set return path back here
            session['ret_path'] = '/create'
            return redirect('/login')

    # Get values passed via POST
    title = request.form.get('title')
    content = request.form.get('content')
    author = util.accounts.get_logged_in_user(session)

    if title is None:
        title = ''
    if content is None:
        content = ''

    post = util.posts.create_post(title, content, author)
    if post is None:  # Did not properly create post
        return redirect('/create')
    return redirect('/post?p={post}'.format(post=post))


@app.route('/post')
def post():
    # Get values passed via GET
    post = request.args.get('p')
    post_list = [util.posts.get_formatted_post(post)]
    return render_template(
        'post_mult.html',
        posts=post_list
    )


@app.route('/author/<author>')
def author(author):
    ids = util.posts.get_author_posts(author)
    post_list = [util.posts.get_formatted_post(post_id) for post_id in ids]
    return render_template(
        'post_mult.html',
        posts=post_list
    )


@app.route('/home')
def home():
    # Get values passed via GET
    ids = util.posts.get_all_posts()
    post_list = [util.posts.get_formatted_post(post_id) for post_id in ids]
    print(post_list)
    return render_template(
        'post_mult.html',
        posts=post_list
    )


if __name__ == '__main__':
    util.posts.create_table()
    util.accounts.create_table()
    app.debug = True  # Set to `False` before release
    app.run()

