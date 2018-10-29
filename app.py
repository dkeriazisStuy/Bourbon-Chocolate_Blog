from flask import Flask, request, render_template, session, redirect, flash
import util.accounts
import util.posts
import util.sessions
import util.search
import base64

app = Flask(__name__)
app.secret_key = util.accounts.get_salt()


@app.route('/')
def index():
    util.sessions.clear_ret_path(session)
    ids = util.posts.get_all_posts()
    post_list = [util.posts.get_formatted_post(post_id) for post_id in ids]
    #print(post_list)
    if util.accounts.is_logged_in(session):
        return render_template(
            'index_user.html',
            posts=post_list,
            logged_in=util.accounts.get_logged_in_user(session)
        )
    else:
        return render_template(
            'index_anon.html',
            posts=post_list,
            logged_in=None
        )


@app.route('/search')
def search():
    util.sessions.clear_ret_path(session)
    ids = util.posts.get_all_posts()

    if 'q' not in request.args:
        query = ''
    else:
        query = request.args.get('q')

    scored_tuples = []
    for post in ids:
        title, content, _, _ = util.posts.get_post(post)
        content_score = util.search.score(content, query)
        title_score = util.search.score(title, query)
        score = title_score + content_score
        if score > 2 * len(query):
            scored_tuples.append((score, post))

    def get_first(element):
        return element[0]

    ranked_tuples = sorted(scored_tuples, key=get_first, reverse=True)
    #  print(ranked_tuples)
    if len(ranked_tuples) > 0:
        high_score = ranked_tuples[0][0]
    else:
        high_score = 0

    filtered_tuples = []
    for score, post in ranked_tuples:
        if score >= 0.4 * high_score:
            filtered_tuples.append((score, post))

    post_list = [
        util.posts.get_formatted_post(post) for _, post in filtered_tuples
    ]
    return render_template(
        'search.html',
        posts=post_list,
        query=query,
        result_count=len(post_list),
        logged_in=util.accounts.get_logged_in_user(session)
    )


@app.route('/edit/<post>', methods=['GET', 'POST'])
def edit(post):
    util.sessions.clear_ret_path(session)
    if not util.accounts.is_logged_in(session):
        return redirect('/')
    if request.method == 'GET':
        title, content, author, _ = util.posts.get_post(post)
        if util.accounts.get_logged_in_user(session) == author:
            return render_template(
                'edit.html',
                button_name='Edit Post',
                post=post,
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

    if title is None:
        title = ''
    if content is None:
        content = ''

    util.posts.edit_post(post,title,content)
    return redirect('/post/{post}'.format(post=post))


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

    ret_path = util.sessions.use_ret_path(session)
    if ret_path is None:
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
        ret_path = util.sessions.use_ret_path(session)
        if ret_path is None:
            return redirect('/')
        else:
            return redirect(ret_path)


@app.route('/logout')
def logout():
    util.sessions.clear_ret_path(session)
    util.accounts.logout_user(session)
    return redirect('/')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        if util.accounts.is_logged_in(session):
            return render_template(
                'create.html'
            )
        else:
            # Set return path back here
            util.sessions.set_ret_path(session, '/create')
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
    return redirect('/post/{post}'.format(post=post))


@app.route('/post/<post>')
def post(post):
    post_list = [util.posts.get_formatted_post(post)]
    title, _, author, _ = util.posts.get_post(post)
    page_title = '{title} - {author}'.format(
        title=title,
        author=author
    )
    if util.accounts.is_logged_in(session):
        return render_template(
            'post_mult.html',
            posts=post_list,
            page_title=page_title,
            logged_in=util.accounts.get_logged_in_user(session)
        )
    else:
        return render_template(
            'post_mult.html',
            posts=post_list,
            page_title=page_title,
            logged_in=None
        )


@app.route('/author/<author>')
def author(author):
    util.sessions.clear_ret_path(session)
    ids = util.posts.get_author_posts(author)
    post_list = [util.posts.get_formatted_post(post_id) for post_id in ids]
    return render_template(
        'post_mult.html',
        posts=post_list,
        page_title=author,
        logged_in=util.accounts.get_logged_in_user(session)
    )


@app.route('/delete/<post>')
def delete(post):
    util.sessions.clear_ret_path(session)
    result = util.posts.get_post(post)
    if result is None:
        return redirect('/')

    _, _, author, _ = result
    if util.accounts.get_logged_in_user(session) == author:
        util.posts.delete_post(post)
    return redirect('/')


if __name__ == '__main__':
    util.posts.create_table()
    util.accounts.create_table()
    app.debug = True  # Set to `False` before release
    app.run()

