import sqlite3 
import random
import posts

DB_FILE = "data.db"
if __name__ == "__main__":
    DB_FILE = '../data/' + DB_FILE

db = sqlite3.connect(DB_FILE) # opens or makes the file
c = db.cursor() 


posts.create_table()


posts.create_post("id","title","content","anon")
posts.create_post("ads","ads","content","anon")
posts.create_post("ads1","title","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
posts.create_post("rip","title","content","anon")
posts.create_post("rip1","rip1","content","anon")
posts.create_post("rip2","rip2","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")
posts.create_post(random.SystemRandom().getrandbits(16),"title","content","anon")


posts.get_post("ads")


posts.delete_post("ads")
posts.get_post("ads")
posts.post_exists("oops")
posts.delete_post("oops")
posts.get_post("oops")
posts.delete_post("rip1")
posts.get_post("rip1")
posts.delete_post("rip2")
posts.get_post("rip2")

posts.get_post("ads")


posts.edit_post("ads1", "hi","bye")


db.commit() # saves changes
db.close() # closes db
