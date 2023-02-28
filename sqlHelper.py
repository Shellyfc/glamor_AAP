import sqlite3
from flask import g

DATABASE = '/Users/glamor-sypha/Documents/Glamor/glamor.sqlite'



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def insert(line, params):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(line, params)
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def select(line):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute(line)
    rows = cur.fetchall()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv