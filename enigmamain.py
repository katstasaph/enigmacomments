"""
Created on Mar 18, 2021

@author: katherine
"""
import datetime as dt
import time
import random
import sys
import os
import db
from dotenv import load_dotenv
from cohost.models.user import User
from cohost.models.block import AttachmentBlock, MarkdownBlock

load_dotenv()
COHOST_USER = os.environ.get('COHOST_USER')
COHOST_PASS = os.environ.get('COHOST_PASS')
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

BACKGROUNDS = ['https://staging.cohostcdn.org/attachment/33c314d6-c5ec-448b-810a-dd20195aee0d/mcmxc.jpg',
               'https://staging.cohostcdn.org/attachment/19430492-e923-40e0-83f7-5782bac839c9/cross.jpg',
               'https://staging.cohostcdn.org/attachment/53e0df40-ae2f-4427-a652-4fe9eeb2e8bd/roi.jpg',
               'https://staging.cohostcdn.org/attachment/8a6d7e15-d52f-4aac-94b4-90611ad458c8/screen.jpg',
               'https://staging.cohostcdn.org/attachment/a91c39a4-89e1-42a7-b764-1706a1528cac/post.jpg',
               'https://staging.cohostcdn.org/attachment/df209117-9b0c-408a-aea2-56550dd7d42e/turn.jpg',
               'https://staging.cohostcdn.org/attachment/5eba8bbb-1a60-441e-b93c-9425be72db3b/boum.jpg',
               'https://staging.cohostcdn.org/attachment/d9932c12-ff21-40c5-95c7-f1928ca85302/puerta.jpg',
               'https://staging.cohostcdn.org/attachment/b8af807a-4a77-4df0-843b-720099c0a0a4/amen.jpg',
               'https://staging.cohostcdn.org/attachment/2674b5f3-24b0-4faf-97a6-1e52fdb1412b/mmx.jpg',
               'https://staging.cohostcdn.org/attachment/93691936-32b9-48c3-a1fb-9600348b8270/lsd.jpg',
               'https://staging.cohostcdn.org/attachment/7dcac150-7296-4c24-b501-0c1328d751a0/plat.jpg',
               'https://staging.cohostcdn.org/attachment/0d6e0a41-bc13-4443-822b-b783599b9e67/mea.png',
               'https://staging.cohostcdn.org/attachment/64415604-9e3d-48d1-8120-5c32e153181b/sade2.png']

default_tags = ['enigmacomments', 'enigma', 'music', 'bot', 'internet comments']

tagintervals = {  # The minimum amount of tweets needed between two tweets of same type
    "age": 3,
    "allcaps": 6,
    "alwayssunny": 11,
    "audiophile": 5,
    "casual": 3,
    "chappelle": 11,
    "cosmic": 5,
    "covid": 7,
    "creative": 5,
    "creepy": 4,
    "crush": 7,
    "culturevulture": 4,
    "drive": 5,
    "erowid": 4,
    "exercise": 5,
    "family": 3,
    "generic": 2,
    "grief": 7,
    "gushing": 3,
    "haters": 6,
    "informative": 3,
    "jojo": 11,
    "language": 5,
    "lewd": 4,
    "lifeevents": 5,
    "location": 4,
    "lofibeats": 5,
    "lyrics": 3,
    "manofthehouse": 11,
    "modernworld": 6,
    "musicalelements": 3,
    "negative": 7,
    "nerd": 6,
    "newage": 5,
    "nostalgia": 3,
    "ofortuna": 11,
    "otherartists": 5,
    "othermedia": 5,
    "puremoods": 11,
    "question": 6,
    "religion": 4,
    "satanicpanic": 8,
    "shitpost": 11,
    "specificsongs": 6,
    "srsbns": 4,
    "storytime": 2,
    "techmeta": 5,
    "tobefair": 7,
    "tropicthunder": 11,
    "verylewd": 11
}

tagcounter = {  # How many tweets have passed since the last tweet of this type
    "age": 0,
    "allcaps": 0,
    "alwayssunny": 0,
    "audiophile": 0,
    "casual": 0,
    "cosmic": 0,
    "covid": 0,
    "creative": 0,
    "creepy": 0,
    "crush": 0,
    "culturevulture": 0,
    "drive": 0,
    "erowid": 0,
    "exercise": 0,
    "family": 0,
    "generic": 0,
    "grief": 0,
    "gushing": 0,
    "haters": 0,
    "informative": 0,
    "jojo": 0,
    "language": 0,
    "lewd": 0,
    "lifeevents": 0,
    "location": 0,
    "lofibeats": 0,
    "lyrics": 0,
    "manofthehouse": 0,
    "modernworld": 0,
    "musicalelements": 0,
    "negative": 0,
    "nerd": 0,
    "newage": 0,
    "nostalgia": 0,
    "ofortuna": 0,
    "otherartists": 0,
    "othermedia": 0,
    "puremoods": 0,
    "question": 0,
    "religion": 0,
    "satanicpanic": 0,
    "shitpost": 0,
    "specificsongs": 0,
    "srsbns": 0,
    "storytime": 0,
    "techmeta": 0,
    "tobefair": 0,
    "verylewd": 0
}

def choose_tweet():
    i = 0
    while (True):
        i += 1  # How many attempts we have to choose a tweet, will break if we have too many failed tries
        chosen_tweet = db.choose_tweet();
        if not can_tweet_post_now(chosen_tweet[2]):
            print("Timebound tweet {} no good. Rerolling...".format(chosen_tweet[1]))
            continue
        for tag in chosen_tweet[2]:
            current_interval = tagcounter.get(tag)
            required_interval = tagintervals.get(tag)
            if current_interval and current_interval < required_interval:
                print("'{}' no good. Rerolling...".format(chosen_tweet[1]))
                break
            if i > 10:
                return chosen_tweet  # Failsafe
            return chosen_tweet

# to do - change this ungodly mess from exclusionary to inclusionary
# i.e., start a blank hash/dictionary, add valid times to it for each tag, build it up

def can_tweet_post_now(tags):
    valid = valid_time_ranges(tags)
    now = dt.datetime.now()
    today = dt.date.today()
    return valid_time(valid["times"], now.time()) and valid_date(valid["dates"], today)

def valid_time(time_ranges, now):
    if len(time_ranges) == 0:
        return True
    for range in time_ranges:
        start = dt.time(range[0], 0)
        end = dt.time(range[1], 59)
        if now >= start and now <= end:
            return True
    return False

def valid_date(date_ranges, today):
    if len(date_ranges) == 0:
        return True
    for range in date_ranges:
        start = dt.date(today.year, range[0], range[1])
        end = dt.date(today.year, range[2], range[3])
        if today >= start and today <= end:
            return True
    return False

def valid_time_ranges(tags):
    time_range = {"times": [], "dates": []}
    for tag in sorted(tags):
        if tag == "afternoon":
            time_range["times"].append((12, 17))
        if tag == "evening":
            time_range["times"].append((16, 23))
        if tag == "morning":
            time_range["times"].append((6, 11))
        if tag == "night":
            time_range["times"].append((16, 23))
            time_range["times"].append((0, 2))
        # this is why we sorted, so we can overwrite any other intervals
        if tag == "verylewd":
            time_range["times"] = [19, 3]
        if tag == "christmas":
            time_range["dates"].append((12, 24, 12, 25))
        if tag == "halloween":
            time_range["dates"].append((10, 30, 10, 31))
        if tag == "newyear":
            time_range["dates"].append((1, 1, 1, 1))
            time_range["dates"].append((12, 31, 12, 31))
        if tag == "valentines":
            time_range["dates"].append((2, 14, 2, 14))
        if tag == "spring":
            time_range["dates"].append((3, 20, 6, 19))
        if tag == "summer":
            time_range["dates"].append((6, 20, 9, 21))
        if tag == "autumn":
            time_range["dates"].append((9, 22, 12, 20))
        if tag == "winter":
            time_range["dates"].append((12, 21, 12, 31))
            time_range["dates"].append((1, 1, 3, 19))
    return merge(time_range)

def merge(time_range):
    if not time_range["dates"]:
        return time_range
    time_range["dates"] = merge_date_range(time_range["dates"])
    return time_range

def merge_date_range(dates):
    new_dates = sorted(dates, key=itemgetter(0, 1))
    compressed = [list(new_dates[0])]
    for date in new_dates:
        date = list(date)
        if (date[0] <= compressed[-1][2]):
            compressed[-1][2] = max(date[2], compressed[-1][2])
            compressed[-1][3] = date[3]
        else:
            compressed.append(date)
    return compressed

def update_tweet_counters(tags):
    for key, value in tagcounter.items():
        if key in tags:
            tagcounter[key] = 1
        elif not value:
            continue
        else:
            tagcounter[key] += 1
    print(f"{tagcounter}")

def get_content_warnings(tags):
  cws = []
  if 'verylewd' in tags:
    cws.append('sex')
    cws.append('lewdness')
  if 'erowid' in tags:
    cws.append('drugs')
  if 'grief' in tags:
    cws.append('grief')
  return cws

while True:
    user = User.login(COHOST_USER, COHOST_PASS)
    project = user.getProject('enigmacomments')
    print('Logged in as: {}'.format(project))
    if not valid_time([(4, 7)], dt.datetime.now().time()):
        chosen_tweet = choose_tweet();
        id = chosen_tweet[0]
        text = chosen_tweet[1]
        tags = chosen_tweet[2]
        update_tweet_counters(tags)
        print("Tweet chosen: {}".format(text))
        chosen_background = random.choice(BACKGROUNDS)
        css_crime_start = '<div style="background-image: url(\'' + chosen_background + '\'); height: 600px; background-size: cover; opacity: 0.8"> \
                          <div style="background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 1), rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.7)); \
                          border-radius: 0.5em; width: 75%; padding: 5px 5px 5px 5px; text-align: center; position: absolute; top: 75%; left: 50%; \
                          transform: translate(-50%, -50%); color:#FFF; font-size:110%;">'
        css_crime_end = '</div></div>'
        blocks = [
            MarkdownBlock(css_crime_start + text + css_crime_end),
        ]
        cws = get_content_warnings(tags)
        project.post('',
                     blocks,
                     cws,
                     adult=False, draft=False, tags=default_tags)
        time_to_elapse = random.randint(240, 300)
        print(id)
        db.delete_tweet(id)
        print("New tweet in {} minutes.".format(time_to_elapse))
        newtime = dt.datetime.now() + dt.timedelta(minutes=time_to_elapse)
        while dt.datetime.now() < newtime:
            time.sleep(1)
    else:
        time.sleep(1000000) #Roughly 1 2/3 hours
