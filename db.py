import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def repopulate():
    db = psycopg2.connect(database=os.environ.get('TWEET_DB'),
                        host=os.environ.get('PGHOST'),
                        user=os.environ.get('PGUSER'),
                        password=os.environ.get('PGPASS'),
                        port=os.environ.get('PORT'))
    cursor = db.cursor()
    f = open('tweets.json', "r+", encoding="utf-8")
    tweets = json.load(f)
    for tweet in tweets:
        cursor.execute("INSERT INTO tweets (tweet, tags) VALUES (%s, %s::text[])", (tweet['text'], tweet['tags']))
    db.commit()
    cursor.close()
    db.close()

def choose_tweet():
    db = psycopg2.connect(database=os.environ.get('TWEET_DB'),
                        host=os.environ.get('PGHOST'),
                        user=os.environ.get('PGUSER'),
                        password=os.environ.get('PGPASS'),
                        port=os.environ.get('PORT'))
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tweets TABLESAMPLE SYSTEM_ROWS(1)")
    tweet = cursor.fetchone()
    cursor.close()
    db.close()
    return tweet

def delete_tweet(id):
    db = psycopg2.connect(database=os.environ.get('TWEET_DB'),
                        host=os.environ.get('PGHOST'),
                        user=os.environ.get('PGUSER'),
                        password=os.environ.get('PGPASS'),
                        port=os.environ.get('PORT'))
    cursor = db.cursor()
    cursor.execute("DELETE FROM tweets WHERE id = %s;", (id,))
    db.commit()
    cursor.close()
    db.close()