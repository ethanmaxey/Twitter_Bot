import tweepy
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('key'), os.getenv('secret'))
api = tweepy.API(auth)

triggers = ["radical democrats", "impeach biden", "joe biden's america", "biden's america", "nazi's", "nazi",
            "illegals", "regime", "trans-terrorism", "trump", "left-wing", "the establishment", "the far left",
            "wacktivism", "president trump", "taking our guns", "lgb", "let's go brandon", "lets go brandon",
            "targeted conservatives", "the left", "higher than hunter", "sleepy joe", "me too'd", "wall",
            "build a wall", "america first", "dems", "fauci", "christianity", "woke politics", "woke",
            "stolen from president trump", "not telling the ", "truth", "election integrity", "gas prices",
            "president trump", "return to god"]

following = tweepy.Cursor(api.get_friends).items()
count = 1
while True:
    for friend in following:
        user_id = friend._json['id']
        statuses = api.user_timeline(screen_name=friend.screen_name, count=count, since_id=count,
                                     tweet_mode="extended")

        for status in statuses:
            exact_tweet_time = status._json['created_at']
            formatted_datetime = datetime.strftime(datetime.strptime(exact_tweet_time, '%a %b %d %H:%M:%S +0000 %Y'),
                                                   '%Y-%m-%d')
            current_time = datetime.date(datetime.today())

            contains = any(element in status.full_text.lower() for element in triggers)  # Produces boolean

            if str(formatted_datetime) == str(current_time) and contains:
                try:
                    api.retweet(status.id)
                    print(f"Retweeting {friend.name}:\n {status.full_text}")
                    time.sleep(15)
                except tweepy.errors.Forbidden:
                    print(f"\nALREADY RETWEETED {friend.name}'s IGNORANT TWEET")