import random
import sqlite3
import time
import util.config


def get_db():
    """Prints all rows in posts"""
    db, c = util.config.start_db()
    c.execute("SELECT * FROM posts")
    print(c.fetchall())
    util.config.end_db(db)


def create_table():
    """Makes 'posts' table in data.db"""
    db, c = util.config.start_db()
    try:
        c.execute(
            '''CREATE TABLE posts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                time INT NOT NULL
            )'''
        )
    except sqlite3.OperationalError:  # if table already exists
        pass
    util.config.end_db(db)


def get_post_id():
    """Returns a random post id"""
    id_length = 16
    return ''.join(
        random.choice(util.config.CHARSET) for _ in range(id_length)
    )


def post_exists(post):
    """Returns whether a post exists"""
    db, c = util.config.start_db()
    c.execute(
        "SELECT EXISTS(SELECT 1 FROM posts WHERE id = ? LIMIT 1)",
        (post,)
    )
    result = c.fetchone()[0]
    util.config.end_db(db)
    return result == 1


def author_exists(author):
    """Returns whether an author exists"""
    db, c = util.config.start_db()
    c.execute(
        "SELECT EXISTS(SELECT 1 FROM posts WHERE author = ? LIMIT 1)",
        (author,)
    )
    result = c.fetchone()[0]
    util.config.end_db(db)
    return result == 1


def create_post(title, content, author):
    """Adds (creates) a post to 'posts'"""
    post = get_post_id()
    db, c = util.config.start_db()
    params = (post, title, content, author, int(time.time()))
    if title is None or content is None or author is None:
        return None
    print('create_post: {post}\t{title}\t{content}\t{author}'.format(
        post=post,
        title=title,
        content=content,
        author=author
    ))
    c.execute("INSERT INTO posts VALUES (?,?,?,?,?)", params)
    util.config.end_db(db)
    return post


def get_post(post):
    """Gets a post from 'posts'"""
    db, c = util.config.start_db()
    c.execute(
        "SELECT title, content, author, time FROM posts WHERE id = ? LIMIT 1",
        (post,)
    )
    result = c.fetchone()
    util.config.end_db(db)
    return result


def get_formatted_post(post):
    """Gets a post with proper formatting"""
    title, content, author, timestamp = get_post(post)
    content = render_post(content)
    # Format: 'Jan 2, 2003 04:05:06'
    time_str = time.strftime('%b %d, %Y %H:%M:%S', time.localtime(timestamp))
    return post, title, content, author, time_str


def get_author_posts(author):
    """Returns ids of all posts by an author"""
    db, c = util.config.start_db()
    c.execute('''
        SELECT id
        FROM posts
        WHERE author = ?
        ORDER BY time DESC
        ''', (author,))
    result = c.fetchall()
    util.config.end_db(db)
    ids = [i[0] for i in result]
    print(ids)
    return ids


def get_all_posts():
    """Returns ids of all posts"""
    db, c = util.config.start_db()
    c.execute("SELECT id FROM posts ORDER BY time DESC")
    result = c.fetchall()
    util.config.end_db(db)
    ids = [i[0] for i in result]
    return ids


def delete_post(post):
    """Deletes a post from 'posts'"""
    if post_exists(post): # if the post exists, delete it
        db, c = util.config.start_db()
        c.execute("DELETE FROM posts WHERE id = ?", (post,))
        util.config.end_db(db)
        print("delete_post: " + post) # see that it runs, comment out later
        return True
    else: # if the post doesn't exist
        print(":P post " + post + " doesn't exist")
        return False


def edit_post(post, title, content):
    """Edits a post from 'posts'"""
    if post is None or title is None or content is None:
        return False
    if post_exists(post): # if the post exists, edit it
        db, c = util.config.start_db()
        c.execute(
            "UPDATE posts SET title = (?), content = (?)  WHERE id = (?)",
            (title, content, post)
        )
        util.config.end_db(db)
        return True
    else:
        return False


def render_post(content):
    """Formats post content from raw text to html"""
    replacements = (
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('\n', '<br>'),
    )
    for key, val in replacements:
        content = content.replace(key, val)
    return content


if __name__ == "__main__":
    create_table()
    db_file()
    get_db()
    create_post('title', 'content', 'anon')
    create_post('ads', 'content', 'anon')
    create_post('title', 'content', 'anon')
    create_post('title', 'content', 'anon')
    print("\nCURRENT DATABASE")
    get_db()

