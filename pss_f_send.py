import sqlite3
def setup_db():
    conn=sqlite3.connect('psses.db')
    cursor=conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT,
    username TEXT,
    password BLOB
)
""")
    conn.commit()
    conn.close()

def send(ref,uname,paswd):
    conn=sqlite3.connect('psses.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",(ref, uname, paswd))
    conn.commit()
    conn.close()


def receive(ref,uname=None):
    conn=sqlite3.connect('psses.db')
    cur=conn.cursor()
    if uname:
        cur.execute('select * from passwords where service=? AND uname=?',(ref,uname))
    else:
        cur.execute('select * from passwords where service=?',(ref,))
    l=cur.fetchall()
    conn.commit()
    conn.close()
    return l

def delete(ref,uname=None):
    conn=sqlite3.connect('psses.db')
    cur=conn.cursor()
    if uname:
        cur.execute('delete from passwords where service=? AND uname=?',(ref,uname))
    else:
        cur.execute("delete from passwords where service=?", (ref,))
    conn.commit()
    conn.close()