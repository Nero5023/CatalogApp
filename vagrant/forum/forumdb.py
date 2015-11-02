	#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection

# Get posts from database.
def GetAllPosts():
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute("SELECT time, content FROM posts ORDER BY time DESC")
    posts = ({'content': str(row[1]), 'time': str(row[0])} 
    		  for row in c.fetchall())
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    # cleanContent = bleach.clean(content)
    c.execute("INSERT INTO posts (content) VALUES(%s)" ,(content,))
    #t = time.strftime('%c', time.localtime())
    DB.commit()
    DB.close()

# DB = []

# def GetAllPosts():
#     conn = psycopg2.connect("dbname=forum")
#     cursor = conn.cursor()
#     cursor.execute("SELECT time, content FROM posts ORDER BY time DESC")
#     DB = cursor.fetchall()
#     posts = [{'content': str(row[1]),
#             'time': str(row[0])} for row in DB]
#     # posts.sort(key=lambda row: row['time'], reverse=True)
#     conn.close()
#     return posts

# def AddPost(content):
#     t = time.strftime('%c', time.localtime())
#     DB.append((t, content))
#     conn = psycopg2.connect("dbname=forum")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO posts (content) VALUES(%s)" ,(content,))
#     conn.commit()
#     conn.close()

   





#     FETCHQUERY = "SELECT id FROM posts ORDER BY id DESC limit 1"
#     cursor.execute(FETCHQUERY)
#     result = cursor.fetchall()
#     max_id = result[0][0]
#     INSERTQUERY = "INSERT into posts (content, time, id) VALUES(%s, %c, %d)" % (content, t, max_id+1)
#     cursor.execute(INSERTQUERY)
#     cursor.commit()
#     conn.close()

