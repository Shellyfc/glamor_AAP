from dao.onlineResult import *

if __name__ == '__main__':
    updateAnswerOnlineResult(1, None, "MODEL", "ANSWER")
    q0 = queryAnswerOnlineResultWithIdAndModel(bid=1, did=None, model="MODEL")
    q0 = queryTopOnlineResult(bid=1, did=None, model="MODEL")
    q1 = queryDataB("testA", "testC", "testD")
    q2 = queryDataD("testA", "testB", "testC")
    i1 = insertDataB("testA", "testC", "testD")
    i2 = insertDataD("testA", "testB", "testC")

    q3 = queryDataB("testA", "testC", "testD")
    q4 = queryDataD("testA", "testB", "testC")


