import sqlite3

conn = sqlite3.connect('site.db')
cur = conn.cursor()

cur.execute("SELECT * FROM user")
users = cur.fetchall()

for user in users:
    print(user)

conn.close()
