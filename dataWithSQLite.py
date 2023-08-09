import os
import random

from dao.onlineResult import *
from simple import gensimWord2Vec, findIndexAndTrueScore, findIndexHF, getRawQuestions, calculateScore

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import torch
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from transformers import BertModel, BertConfig, BertTokenizer, FlaxBertForQuestionAnswering, pipeline
import gensim
from transformers import logging
from datetime import datetime
from random import sample, choices
import sqlite3
import dao
import sys

logging.set_verbosity_error()

DATASET_PATH = './GoogleNews-vectors-negative300.bin'

# Initializing a BERT bert-base-uncased style configuration
configuration = BertConfig()

# Initializing a model from the bert-base-uncased style configuration
model = BertModel(configuration)

# Accessing the model configuration
configuration = model.config
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
# logging.getLogger('flask_cors').level = logging.DEBUG

# # Connecting to the SQLite
# conn = sqlite3.connect('glamor.db')
# print("Opened database successfully")
DATABASE = './glamor.sqlite'


def printConfig():
    print(f"PyTorch version: {torch.__version__}")

    # Check PyTorch has access to MPS (Metal Performance Shader, Apple's GPU architecture)
    print(f"Is MPS (Metal Performance Shader) built? {torch.backends.mps.is_built()}")
    print(f"Is MPS available? {torch.backends.mps.is_available()}")

    # Set the device
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f"Using device: {device}")


def searchOnline(bid, did, model, formA, formB, formC, formD):
    """
    search for model with entries, cache result into top & answer
    @param searchB:
    @param model:
    @param formA:
    @param formB:
    @param formC:
    @param formD:
    @return:
    """
    sentence = "{A} is to {B} as {C} is to {D}."
    mask = 'NoneNone'
    if model == 'gensim':
        gensimD, gensimB = gensimWord2Vec(formA, formB, formC, formD)
        if bid:
            gensim = gensimB
            top, topScore = gensim[0]
            topSentence = sentence.format(A=formA, B='*' + top, C=formC, D=formD)
            answerSentence = sentence.format(A=formA, B='*' + formB, C=formC, D=formD)
            answer = formB
        elif did:
            gensim = gensimD
            top, topScore = gensim[0]
            topSentence = sentence.format(A=formA, B=formB, C=formC, D='*' + top)
            answerSentence = sentence.format(A=formA, B=formB, C=formC, D='*' + formD)
            answer = formD
        answerIdx, answerScore = findIndexAndTrueScore(gensim, answer)
        answerRank = 1.0 / (answerIdx + 1) if answerIdx is not None else 'NA'
        return {'model': model, 'top': top, 'topScore': topScore, 'topRank': 1.0,
                'topSentence': topSentence,
                'answer': answer,
                'answerScore': answerScore,
                'answerRank': answerRank,
                'answerSentence': answerSentence}
    elif model == 'bert-base-uncased' or model == 'vocab-transformers/distilbert-word2vec_256k-MLM_1M':
        mask = '[MASK]'
    elif model == 'roberta-base' or model == 'roberta-large':
        mask = '<mask>'

    if bid:
        tmp = sentence.format(A=formA, B=mask, C=formC, D=formD)
        answer = formB
    else:
        tmp = sentence.format(A=formA, B=formB, C=formC, D=mask)
        answer = formD

    unmasker = pipeline('fill-mask', model=model, top_k=2000, device=torch.device("mps"))
    if mask in tmp:
        tmpResult = unmasker(tmp)
        top, topScore = tmpResult[0]['token_str'], tmpResult[0]['score']
        answerScore = unmasker(tmp, targets=answer)[0]['score']
        if model.startswith('roberta'):
            answerScore = max(answerScore, unmasker(tmp, targets=" " + answer)[0]['score'],
                              unmasker(tmp, targets=answer + " ")[0]['score'])
        idx = findIndexHF(tmpResult, answer)
        reciprocalRank = 1.0 / (idx + 1) if idx is not None else 'NA'
        ret = {'model': model, 'top': top, 'topScore': topScore, 'topRank': 1.0,
               'topSentence': tmp.replace(mask, "*" + top), 'answer': answer,
               'answerScore': answerScore,
               'answerRank': reciprocalRank, 'answerSentence': tmp.replace(mask, "*" + answer)}
    return ret


@app.post('/table/queryOnlineResult')
# @cross_origin()
def queryOnlineResult():
    """

    @return:{B: [{}, {}, {}], D:[{}, {}, {}]}
    """
    content = request.get_json(force=True)
    print(content)
    sentence = "{A} is to {B} as {C} is to {D}."
    models = ['bert-base-uncased', 'roberta-base', 'roberta-large',
              'vocab-transformers/distilbert-word2vec_256k-MLM_1M', 'gensim']
    result = {'B': [], 'D': []}  # {B: [{}, {}, {}], D:[{}, {}, {}]}
    email = content.get('email')
    formA = content.get('formA')
    formB = content.get('formB')
    formC = content.get('formC')
    formD = content.get('formD')
    print(email, formA, formB, formC, formD)
    for model in models:
        rowB = queryDataBWithInput(formA, formC, formD)
        rowD = queryDataDWithInput(formA, formB, formC)
        if rowB != None:
            bid = rowB[0]
            topB = queryTopOnlineResult(bid=bid, did=None, model=model)
            answerB = queryAnswerWithIDAndAnswer(bid=bid, did=None, answer=formB)
            if answerB:
                aid = answerB[0]
                answerBWithModel = queryAnswerOnlineResultWithAIDAndModel(aid, model)
            if not topB or not answerB or not answerBWithModel:
                top_answer_both = searchOnline(bid, None, model, formA, formB, formC, formD)
                result['B'].append(top_answer_both)
                insertTopOnlineResult(bid, None, model, top_answer_both['top'], top_answer_both['topRank'],
                                      top_answer_both['topScore'], top_answer_both['topSentence'])
                aid = user_answer(email, bid, None, top_answer_both['answer'], top_answer_both['answerSentence'])
                insertAnswerOnlineResult(aid, model, top_answer_both['answer'], top_answer_both['answerRank'],
                                         top_answer_both['answerScore'])
            else:
                result['B'].append({'model': model, 'top': topB[4], 'topScore': topB[6], 'topRank': topB[5],
                                    'topSentence': topB[7],
                                    'answer': answerBWithModel[3],
                                    'answerScore': answerBWithModel[5],
                                    'answerRank': answerBWithModel[4],
                                    'answerSentence': answerB[4]})
        else:
            # complete new question: search online and cache
            bid = insertDataB(formA, formC, formD)
            top_answer_both = searchOnline(bid, None, model, formA, formB, formC, formD)
            insertTopOnlineResult(bid, None, model, top_answer_both['top'], top_answer_both['topRank'],
                                  top_answer_both['topScore'], top_answer_both['topSentence'])
            result['B'].append({'model': model, 'top': top_answer_both['top'], 'topScore': top_answer_both['topScore'],
                                'topRank': top_answer_both['topRank'],
                                'topSentence': top_answer_both['topSentence'],
                                'answer': top_answer_both['answer'],
                                'answerScore': top_answer_both['answerScore'],
                                'answerRank': top_answer_both['answerRank'],
                                'answerSentence': top_answer_both['answerSentence']})
        if rowD != None:
            did = rowD[0]
            topD = queryTopOnlineResult(bid=None, did=did, model=model)
            answerD = queryAnswerWithIDAndAnswer(bid=None, did=did, answer=formD)
            if answerD:
                aid = answerD[0]
                answerDWithModel = queryAnswerOnlineResultWithAIDAndModel(aid, model)
            if not topD or not answerD or not answerDWithModel:
                top_answer_both = searchOnline(None, did, model, formA, formB, formC, formD)
                result['D'].append(top_answer_both)
                insertTopOnlineResult(None, did, model, top_answer_both['top'], top_answer_both['topRank'],
                                      top_answer_both['topScore'], top_answer_both['topSentence'])
                aid = user_answer(email, None, did, top_answer_both['answer'], top_answer_both['answerSentence'])
                insertAnswerOnlineResult(aid, model, top_answer_both['answer'], top_answer_both['answerRank'],
                                         top_answer_both['answerScore'])
            else:
                result['D'].append({'model': model, 'top': topD[4], 'topScore': topD[6], 'topRank': topD[5],
                                    'topSentence': topD[7],
                                    'answer': answerDWithModel[3],
                                    'answerScore': answerDWithModel[5],
                                    'answerRank': answerDWithModel[4],
                                    'answerSentence': answerD[4]})
        else:
            # complete new question: search online and cache
            did = insertDataD(formA, formB, formC)
            top_answer_both = searchOnline(None, did, model, formA, formB, formC, formD)
            insertTopOnlineResult(None, did, model, top_answer_both['top'], top_answer_both['topRank'],
                                  top_answer_both['topScore'], top_answer_both['topSentence'])
            result['D'].append({'model': model, 'top': top_answer_both['top'], 'topScore': top_answer_both['topScore'],
                                'topRank': top_answer_both['topRank'],
                                'topSentence': top_answer_both['topSentence'],
                                'answer': top_answer_both['answer'],
                                'answerScore': top_answer_both['answerScore'],
                                'answerRank': top_answer_both['answerRank'],
                                'answerSentence': top_answer_both['answerSentence']})
    return result


@app.post('/table/questions')
@app.post('/play/questions')
# @cross_origin()
def questions():
    num = request.get_json(silent=True).get("num")
    questionsB = queryDataB(num // 2)

    questionsD = queryDataD(num - num // 2)
    questionsD = sample(questionsD, min(num // 2, len(questionsD)))
    ret = []
    sentence = "{A} is to {B} as {C} is to {D}."
    for q in questionsB:
        ret.append({"question": sentence.format(A=q[1], B="______", C=q[2], D=q[3]), "type": "B"})
    for q in questionsD:
        ret.append({"question": sentence.format(A=q[1], B=q[2], C=q[3], D="______"), "type": "D"})
    return ret


def updateAnswerOnVote(aid):
    vote = countAnswerVoteWithAID(aid)
    updateAnswerOnVoteWithAID(aid, vote)


def user_answer(email, bid, did, answer, sentence) -> int:
    """
    1. check if answer exists
    2. if yes, insert into user_answer table & update vote in answer table
    3. if no, insert into answer table and get aid, then insert into user_answer table
    @param email:
    @param bid:
    @param did:
    @param answer:
    @param sentence:
    @return: aid
    """
    if bid:
        AnswerEntity = queryAnswerWithIDAndAnswer(bid, None, answer)
        if AnswerEntity:
            aid = AnswerEntity[0]
            insertUserAnswer(aid, email)
            updateAnswerOnVote(aid)
        else:
            aid = insertAnswer(bid, None, answer, sentence, 1, email)
            insertUserAnswer(aid, email)
            updateAnswerOnVote(aid)
    if did:
        AnswerEntity = queryAnswerWithIDAndAnswer(None, did, answer)
        if AnswerEntity:
            aid = AnswerEntity[0]
            insertUserAnswer(aid, email)
            updateAnswerOnVote(aid)
        else:
            aid = insertAnswer(None, did, answer, sentence, 1, email)
            insertUserAnswer(aid, email)
            updateAnswerOnVote(aid)
    return aid


@app.post('/table/answer')
@app.post('/play/answer')
# @cross_origin()
def answer():
    """
    update user_answer & recalculate vote and then update vote in answer_online_result
    1. check if the answer exits
    2. check if user_answer exits
    3. update vote
    @return: 5 other top voted answers
    """
    content = request.get_json(silent=True)
    email = content.get("email")
    answer = content.get("answer")
    question = content.get("question")
    tmp = question['question'].split()
    sentence = "{A} is to {B} as {C} is to {D}."
    if question['type'] == "B":
        A = tmp[0]
        C = tmp[5]
        D = tmp[8]
        D = D[:len(D) - 1]
        bid = queryDataBWithInput(A, C, D)[0]
        aid = user_answer(email, bid, None, answer, sentence.format(A=A, B='*' + answer, C=C, D=D))
        topAnswers = queryTopVotedAnswersWithid(bid, None, 5)
    elif question['type'] == "D":
        A = tmp[0]
        B = tmp[3]
        C = tmp[5]
        did = queryDataDWithInput(A, B, C)[0]
        aid = user_answer(email, None, did, answer, sentence.format(A=A, B=B, C=C, D='*' + answer))
        topAnswers = queryTopVotedAnswersWithid(None, did, 5)
    return topAnswers


if __name__ == '__main__':
    printConfig()
    port = 8888
    if sys.argv[1]:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)
