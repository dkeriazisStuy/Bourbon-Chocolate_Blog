import random
import posts

def post_exists_msg(id,exists):
    if exists:
        print (id + " exists? " + str(exists))

posts.create_table()
        
posts.db_file()

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
posts.get_author_posts("anon")
posts.get_author_posts("nobody")
print("does author anon exist? " + str(posts.author_exists("anon")))
print("does author nobody exist? " + str(posts.author_exists("nobody")))


posts.delete_post("ads")
posts.get_post("ads")
post_exists_msg("oops",posts.post_exists("oops"))
posts.delete_post("oops")
posts.get_post("oops")
posts.delete_post("rip1")
posts.get_post("rip1")
posts.delete_post("rip2")
posts.get_post("rip2")
posts.get_post("ads")


posts.edit_post("ads1", "hi","bye")
posts.edit_post("oops", "hi","bye")


posts.get_db()

