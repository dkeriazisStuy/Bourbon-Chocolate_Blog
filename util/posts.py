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


# adds (creates) a post to posts
def create_post(id, title, content, author):
    params = (id, title, content, author)
    c.execute("INSERT INTO posts VALUES (?,?,?,?)", params)
    print ("create_post: " + str(id) + "\t" + title + "\t" + content + "\t" + author) # see that it runs, comment out later


# gets a post from posts
def get_post(id):
    params = (id)
    c.execute("SELECT * FROM posts WHERE id = ?;", (params,))
    print ("get_post: " + id) # see that it runs, comment out later
    print(c.fetchall()) # just printing c.fetchall() for now -- will fix later 
    

# deletes a post from posts
def delete_post(title):
    params = (title)
    c.execute("DELETE FROM posts WHERE title = ?;", (params,))
    print("delete_post: " + title) # see that it runs, comment out later


# edits a post from posts
def edit_post(id, title, content):
    params = (title, content, id)
    c.execute("UPDATE posts SET title = (?), content = (?)  WHERE id = (?);", params)
    print("edited: " + id + "\t" + title + "\t" + content) # see that it runs, comment out later



# tests
def tests(): 
    create_post("id","title","content","anon")
    create_post("ads","ads","content","anon")
    create_post("ads1","title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    create_post("rip","title","content","anon")
    create_post("rip1","rip1","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
    get_post("ads")
    delete_post("ads")
    delete_post("oops")
    delete_post("rip1")
    edit_post("ads1", "hi","bye")



def main():
    create_table()
    tests()
    db.commit() # saves changes
    db.close() # closes db


if __name__ == "__main__":
    main()




# print (time.strftime("%y%m%d%H%M%S") + str(random.randint(10001,100000)))
