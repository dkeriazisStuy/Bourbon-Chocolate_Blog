import sqlite3 
import random, time


DB_FILE = "data.db"
if __name__ == "__main__":
    DB_FILE = '../data/' + DB_FILE

db = sqlite3.connect(DB_FILE) # opens or makes the file
c = db.cursor() 



# makes posts table in data.db
def create_table():
    try:
        c.execute("CREATE TABLE posts (id TEXT, title TEXT, content TEXT, author TEXT);")
    except:
        pass


# determines if post exists
def post_exists(id): 
    c.execute("SELECT EXISTS(SELECT 1 FROM posts WHERE id = ? LIMIT 1)", (id,))
    result = c.fetchone()[0]
    print (id + " exists? " + str(result == 1))
    return result == 1


# adds (creates) a post to posts
def create_post(id, title, content, author):
    params = (id, title, content, author)
    c.execute("INSERT INTO posts VALUES (?,?,?,?)", params)
    print ("create_post: " + str(id) + "\t" + title + "\t" + content + "\t" + author) # see that it runs, comment out later


# gets a post from posts
def get_post(id):
    c.execute("SELECT * FROM posts WHERE id = ?;", (id,))
    print ("get_post: " + id + "\t" + str(c.fetchall())) # see that it runs, comment out later
    # print(c.fetchall()) # just printing c.fetchall() for now -- will fix later 
    # should return c.fetchone()
    # c.fetchall() should only return 1 post

    
# deletes a post from posts
def delete_post(id):
    c.execute("DELETE FROM posts WHERE title = ?;", (id,))
    print("delete_post: " + id) # see that it runs, comment out later


# edits a post from posts
def edit_post(id, title, content):
    params = (title, content, id)
    c.execute("UPDATE posts SET title = (?), content = (?)  WHERE id = (?);", params)
    print("edited: " + id + "\t" + title + "\t" + content) # see that it runs, comment out later



def main():
    create_table()
    db.commit() # saves changes
    db.close() # closes db


if __name__ == "__main__":
    main()




# print (time.strftime("%y%m%d%H%M%S") + str(random.randint(10001,100000)))
