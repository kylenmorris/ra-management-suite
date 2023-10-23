import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO announcements (title, content) VALUES (?, ?)",
            ('First Announcement', 'Content for the first announcement')
            )

cur.execute("INSERT INTO announcements (title, content) VALUES (?, ?)",
            ('Second Announcement', 'Content for the second announcement')
            )

connection.commit()
connection.close()
