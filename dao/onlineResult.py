import sqlite3

DATABASE = '/Users/chufang/github/glamor_demo/glamor.sqlite'


def insertDataB(A, C, D) -> int:
    """
    insert one row into data_b
    @param A:
    @param C:
    @param D:
    @return: the id of the row being inserted
    """
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO data_b (A, C, D) VALUES(?, ?, ?)", (A, C, D))
            con.commit()
            msg = "Record successfully added"
            print(cur.lastrowid)
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in insert operation"
        return None
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def insertDataD(A, B, C) -> int:
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO data_d (A, B, C) VALUES(?, ?, ?)", (A, B, C))
            con.commit()
            msg = "Record successfully added"
            print(cur.lastrowid)
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in insert operation"
        return None
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def insertTopOnlineResult(bid, did, model, top, topRank, topScore, topSentence) -> int:
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            if bid:
                cur.execute(
                    "INSERT INTO top_online_result (bid, model, top, topRank, topScore, topSentence) VALUES(?, ?, ?, ?, ?, ?)",
                    (bid, model, top, topRank, topScore, topSentence))
            if did:
                cur.execute(
                    "INSERT INTO top_online_result (did, model, top, topRank, topScore, topSentence) VALUES(?, ?, ?, ?, ?, ?)",
                    (did, model, top, topRank, topScore, topSentence))
            con.commit()
            msg = "Record successfully added"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in insert operation"
        return None
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def insertAnswer(bid, did, answer, answerSentence, vote, createUserEmail):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            if bid:
                cur.execute(
                    "INSERT INTO answer (bid, answer, answerSentence, vote, createUserEmail) VALUES(?, ?, ?, ?, ?)",
                    (bid, answer, answerSentence, vote, createUserEmail))
            if did:
                cur.execute(
                    "INSERT INTO answer (did, answer, answerSentence, vote, createUserEmail) VALUES(?, ?, ?, ?, ?)",
                    (did, answer, answerSentence, vote, createUserEmail))
            con.commit()
            msg = "Record successfully added"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in insert operation"
        return None
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def insertAnswerOnlineResult(aid, model, answer, answerRank, answerScore):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO answer_online_result (aid, model, answer, answerRank, answerScore) VALUES(?, ?, ?, ?, ?)",
                (aid, model, answer, answerRank, answerScore))
            con.commit()
            msg = "Record successfully added"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in insert operation"
        return None
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def insertUserAnswer(aid, email):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO user_answer (aid, email) VALUES(?, ?)",
                (aid, email))
            con.commit()
            msg = "Record successfully added"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in insert operation"
        return None
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def queryDataBWithInput(A, C, D):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM data_b WHERE A = ? AND C = ? AND D = ?", (A, C, D)).fetchone()
    con.close()
    return row


def queryDataDWithInput(A, B, C):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM data_d WHERE A = ? AND B = ? AND C = ?", (A, B, C)).fetchone()
    con.close()
    return row


def queryDataB(num):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM data_b").fetchall()
    con.close()
    return rows


def queryDataD(num):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM data_d").fetchall()
    con.close()
    return rows


def queryTopOnlineResult(bid, did, model):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if bid:
        row = cur.execute("SELECT * FROM top_online_result WHERE bid = ? AND model = ?", (bid, model)).fetchone()
    if did:
        row = cur.execute("SELECT * FROM top_online_result WHERE did = ? AND model = ?", (did, model)).fetchone()
    con.close()
    return row


def queryAnswerWithIDAndAnswer(bid, did, answer):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if bid:
        row = cur.execute("SELECT * FROM answer WHERE bid = ? AND answer = ?", (bid, answer)).fetchone()
    if did:
        row = cur.execute("SELECT * FROM answer WHERE did = ? AND answer = ?", (did, answer)).fetchone()
    con.close()
    return row

def queryTopVotedAnswersWithid(bid, did, num):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if bid:
        rows = cur.execute("SELECT * FROM answer WHERE bid = ? ORDER BY vote DESC", (bid, )).fetchmany(num)
    if did:
        rows = cur.execute("SELECT * FROM answer WHERE did = ? ORDER BY vote DESC", (did,)).fetchmany(num)
    con.close()
    return rows

def queryAnswerOnlineResultWithAIDAndModel(aid, model):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM answer_online_result WHERE aid = ? AND model = ?", (aid, model)).fetchone()
    con.close()
    return rows


def queryAnswerOnlineResult(num):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM answer_online_result").fetchall()
    con.close()
    return rows


def queryAnswerOnlineResultWithIdAndModel(num):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM answer_online_result").fetchall()
    con.close()
    return rows


def queryAnswerOnlineResultWithIdAndModel(bid, did, model):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if bid:
        row = cur.execute("SELECT * FROM answer_online_result WHERE bid = ? AND model = ?", (bid, model)).fetchone()
    elif did:
        row = cur.execute("SELECT * FROM answer_online_result WHERE did = ? AND model = ?", (did, model)).fetchone()
    con.close()
    return row

def updateAnswerOnVoteWithAID(aid, vote):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE answer SET vote = ? WHERE id = ?",
                (vote, aid))
            con.commit()
            msg = "Record successfully updated"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        msg = "error in update operation"
        return -1
    finally:
        con.close()
def updateAnswer(bid, did, answer):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            if bid:
                cur.execute(
                    "UPDATE answer SET vote = vote + 1 WHERE bid = ? AND answer = ?",
                    (bid, answer))
            if did:
                cur.execute(
                    "UPDATE answer SET vote = vote + 1 WHERE did = ? AND answer = ?",
                    (did, answer))
            con.commit()
            msg = "Record successfully updated"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in update operation"
        return -1
    finally:
        con.close()


def updateAnswerOnlineResult(bid, did, model, answer):
    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            if bid:
                cur.execute(
                    "UPDATE answer_online_result SET vote = vote + 1 WHERE bid = ? AND model = ? AND answer = ?",
                    (bid, model, answer))
            if did:
                cur.execute(
                    "UPDATE answer_online_result SET vote = vote + 1 WHERE did = ? AND model = ? AND answer = ?",
                    (did, model, answer))
            con.commit()
            msg = "Record successfully updated"
            return cur.lastrowid
    except sqlite3.Error as err:
        print('Sql error: %s' % (' '.join(err.args)))
        print("Exception class is: ", err.__class__)
        con.rollback()
        msg = "error in update operation"
        return -1
    finally:
        # return render_template("result.html", msg=msg)
        con.close()


def countAnswerVoteWithAID(aid):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    count = cur.execute("SELECT count(*) FROM user_answer WHERE aid = ?", (aid,)).fetchone()[0]
    con.close()
    return count
