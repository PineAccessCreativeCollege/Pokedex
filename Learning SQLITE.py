import sqlite3

conn = sqlite3.connect('login_data.db')

c = conn.cursor()

#c.execute("""CREATE TABLE login_data (
            #uname text,
            #upass text,
            #uid integer
            #)""")

c.execute("INSERT INTO login_data VALUES ('Alex', 'password123', 3262907)")

c.execute("SELECT * FROM login_data WHERE upass='password123'")

print(c.fetchall())

conn.commit()

conn.close()

def Login():
    pass

def ValidateCredentials():
    pass


def AutoLogin():
    pass

