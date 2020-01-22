import os
from collections import defaultdict
from configparser import ConfigParser

import psycopg2 as psycopg2
from flask import Flask, request, abort
from random import randrange
from argparse import ArgumentParser
from spr import PlaySession
from flask_cors import CORS
from heapq import nlargest
import json
from configparser import ConfigParser
import psycopg2.extras


app = Flask(__name__)
CORS(app)

play_sessions = {}
highscores = defaultdict(list)


# region Database


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        db['password'] = os.getenv('DB_PASSWORD')
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


db_params = config()

# endregion


@app.route("/")
def hello_world():
    return "Hello World!"


# GET method receiving 3 parameters:
# user_choice - string, one letter option - r, p, s
# session_id - string, (let's use GUID)
# ai_param - int, moves to remember back 2 or 3, needed only on the first round
#
# method returns string, who won: 'ai', 'player', 'remis' or 'None' if there was an error
# http://127.0.0.1:5000/getRound?user_choice=r&session_id=testtest&ai_param=2
@app.route('/getRound/', methods=['GET'], endpoint='get_round')
def get_round():
    session_id = request.args.get('session_id')
    user_choice = request.args.get('user_choice')
    ai_param = request.args.get('ai_param')

    if session_id not in play_sessions:
        play_sessions[session_id] = PlaySession(session_id, int(ai_param))

    return play_sessions[session_id].play_round(user_choice)


# POST method that receives JSON with name and score properties
@app.route('/saveHighscore/', methods=['POST'], endpoint='save_highscore')
def save_highscore():
    req_data = request.get_json()
    name = req_data['name']
    score = req_data['score']
    if not name:
        abort(400, "name parameter is null")
    if not score:
        abort(400, "score parameter is null")
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        sql = """INSERT INTO highscores
                    (name, score)
                    VALUES (%s, %s);"""
        cur = conn.cursor()
        cur.execute(sql, (name, score))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        abort(500, 'database error')
    finally:
        if conn is not None:
            conn.close()

    return "OK"


# GET method that returns all highscores
@app.route('/getHighscores/', methods=['GET'])
def get_highscores():
    conn = None
    rows = []
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT id, name, score '
                    'FROM highscores '
                    'ORDER BY score DESC '
                    'LIMIT 10')
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return json.dumps(rows)


if __name__ == "__main__":
    parser = ArgumentParser(description="Run server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
