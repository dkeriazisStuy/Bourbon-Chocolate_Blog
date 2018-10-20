import sqlite3
import random, time




def connect_db():
    db = sqlite3.connect("../data/data.db")
    c = db.cursor()
    return db, c


def close_db(db):
    db.commit()
    db.close()


def get_db():
    db, c = connect_db()
    c.execute("SELECT * FROM posts;")
    print(c.fetchall())
    close_db(db)


def db_file():
    db, c = connect_db()
    c.execute("PRAGMA database_list")
    rows = c.fetchall()
    for row in rows:
        print(row[0], row[1], row[2])

        
    

# makes posts table in data.db
def create_table():
    db, c = connect_db()
    try:
        c.execute("CREATE TABLE posts (id TEXT, title TEXT, content TEXT, author TEXT);")
    except:
        pass
    close_db(db)




# determines if post exists
def post_exists(id):
    db, c = connect_db()
    c.execute("SELECT EXISTS(SELECT 1 FROM posts WHERE id = ? LIMIT 1)", (id,))
    result = c.fetchone()[0]
    #print (id + " exists? " + str(result == 1))
    close_db(db)
    return result == 1


# determines if author exists
def author_exists(author):
    db, c = connect_db()
    c.execute("SELECT EXISTS(SELECT 1 FROM posts WHERE author = ? LIMIT 1)", (author,))
    result = c.fetchone()[0]
    #print (id + " exists? " + str(result == 1))
    close_db(db)
    return result == 1




# adds (creates) a post to posts
def create_post(id, title, content, author):
    db, c = connect_db()
    if post_exists(id): # if the post exists already
        print(":P post *" + id + "* exists try again")
        pass
    else:
        params = (id, title, content, author)
        c.execute("INSERT INTO posts VALUES (?,?,?,?)", params)
        print ("create_post: " + str(id) + "\t" + title + "\t" + content + "\t" + author) # see that it runs, comment out later
    close_db(db)


# gets a post from posts
def get_post(id):
    db, c = connect_db()
    if post_exists(id): # if the post exists, get it 
        c.execute("SELECT * FROM posts WHERE id = ?;", (id,))
        rows = c.fetchall()
        for row in rows:
            print(row[0], row[1], row[2], row[3])
            return row[2]
        #print ("get_post: " + id + "\t" + str(c.fetchall())) # see that it runs, comment out later
        # print(c.fetchall()) # just printing c.fetchall() for now -- will fix later 
        # should return c.fetchone()
        # c.fetchall() should only return 1 post
    else: # if the post doesn't exist, do nothing
        pass
    close_db(db)


# gets all of an author's posts from posts
def get_author_posts(author):
    db, c = connect_db()
    if author_exists(author): # if the author exists, get all of their posts
        c.execute("SELECT * FROM posts WHERE author = ?;", (author,))
        print ("get_post: " + author + "\t" + str(c.fetchall())) # see that it runs, comment out later
        # print(c.fetchall())
    else: # if the author doesn't exist
        print("this ain't it chief")
        pass
    close_db(db)


# deletes a post from posts
def delete_post(id):
    db, c = connect_db()
    if post_exists(id): # if the post exists, delete it 
        c.execute("DELETE FROM posts WHERE title = ?;", (id,))
        print("delete_post: " + id) # see that it runs, comment out later
    else: # if the post doesn't exist
        print(":P post " + id + " doesn't exist")
        pass
    close_db(db)


# edits a post from posts
def edit_post(id, title, content):
    db, c = connect_db()
    if post_exists(id): # if the post exists, edit it 
        params = (title, content, id)
        c.execute("UPDATE posts SET title = (?), content = (?)  WHERE id = (?);", params)
        print("edited: " + id + "\t" + title + "\t" + content) # see that it runs, comment out later
    else: # if the post doesn't exist
        print(":P post " + id + " doesn't exist")
        pass
    close_db(db)




if __name__ == "__main__":
    create_table()
    db_file()
    get_db()
    create_post("id","title","content","anon")
    create_post("ads","ads","content","anon")
    create_post("ads1","title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    print("\nCURRENT DATABASE")
    get_db()

# print (time.strftime("%y%m%d%H%M%S") + str(random.randint(10001,100000)))
