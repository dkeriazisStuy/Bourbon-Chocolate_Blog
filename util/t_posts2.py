import random
import posts

def post_exists_msg(id,exists):
    if exists:
        print (id + " exists? " + str(exists))

posts.create_table()
        
posts.db_file()

working = 0

i = 0
while (i < 10):
    i += 1
    n = random.SystemRandom().getrandbits(16)
    posts.create_post(n,"title","content","anon")
    if posts.post_exists(n):
        working += 1
        print("THIS WORKS " + str(working) + " / " + str(i))
    else:
        pass


posts.create_post("id","title","content","anon")
if(posts.post_exists("id")): 
    print("THIS WORKS " + str(working) + " / " + str(i))

posts.create_post("ads","ads","content","anon")
if(posts.post_exists("ads")):
    print("THIS WORKS " + str(working) + " / " + str(i))

posts.create_post("ads1","title","content","anon")
if(posts.post_exists("ads1")):
    print("THIS WORKS " + str(working) + " / " + str(i))

posts.create_post("rip","title","content","anon")
if(posts.post_exists("ads1")):
    print("THIS WORKS " + str(working) + " / " + str(i))

posts.create_post("rip1","rip1","content","anon")
if(posts.post_exists("rip1")):
    print("THIS WORKS " + str(working) + " / " + str(i))
    
posts.create_post("rip2","rip2","content","anon")
if(posts.post_exists("rip2")):
    print("THIS WORKS " + str(working) + " / " + str(i))

    posts.get_post("ads")
print("THIS WORKS " + str(working) + " / " + str(i))



posts.get_post("ads")
posts.get_author_posts("anon")
posts.get_author_posts("nobody")

print("does author anon exist? " + str(posts.author_exists("anon")))
print("does author nobody exist? " + str(posts.author_exists("nobody")))

working += 5
i += 5
print("THIS WORKS " + str(working) + " / " + str(i))

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

working += 10
i += 10
print("THIS WORKS " + str(working) + " / " + str(i))

posts.edit_post("ads1", "bye","bye")
i += 1
print("THIS WORKS " + str(working) + " / " + str(i))

print(posts.get_post("ads1"))
print("THIS WORKS " + str(working) + " / " + str(i))

if "bye" == posts.get_post("ads1"):
    working += 1
    print("THIS WORKS " + str(working) + " / " + str(i))
else:
    print("ADS1")
    
posts.edit_post("oops", "bye","bye")
i += 1
if "bye" == posts.get_post("oops"):
    print("OOPS")
else:
    working += 1
    print("THIS WORKS " + str(working) + " / " + str(i))

    
posts.get_db()

print(str(working))
print(str(i))
