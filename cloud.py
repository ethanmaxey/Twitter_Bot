import tweepy
from datetime import datetime

# Adding parameters to main did not work
def main():
    consumer_key = get_secrets("consumer_key")
    consumer_secret = get_secrets("consumer_secret")
    key = get_secrets("key")
    secret = get_secrets("secret")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)

    triggers = ["this", "is", "a", "list", "of", "keywords"]

    following = tweepy.Cursor(api.get_friends).items()
    count = 1

    # Iterates over all the people the bot follows
    for friend in following:
        statuses = api.user_timeline(screen_name=friend.screen_name, count=count, since_id=count,
                                     tweet_mode="extended")

        # Iterates over each most recent tweet of each person I follow
        for status in statuses:
            exact_tweet_time = status._json['created_at']
            formatted_datetime = datetime.strftime(datetime.strptime(exact_tweet_time,
                                                                     '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d')
            current_time = datetime.date(datetime.today())

            contains = any(element in status.full_text.lower() for element in triggers)  # Produces boolean

            # If the date posted is today and there is a trigger word in the tweet, do the following
            if str(formatted_datetime) == str(current_time) and contains:
                try:
                    api.retweet(status.id)
                    api.update_status(status='cringe', in_reply_to_status_id=status.id,
                                      auto_populate_reply_metadata=True)
                    print(f"Retweeting {friend.name}:\n {status.full_text}")
                except tweepy.errors.Forbidden:
                    print(f"\nALREADY RETWEETED {friend.name}'s TWEET")


if __name__ == "__main__":
    main()
