import tweepy, time, random
from credentials import *
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

filename = open('batch_1.txt','r')
tweettext = filename.read()
filename.close()

bot_output = tweettext.split('====================')
tweeted = []

for tweet in bot_output:
    if len(tweet) <= 280:
        if tweet not in tweeted:
            try:
                api.update_status(tweet)
                tweeted.append(tweet)
            except tweepy.TweepError as error:
                if error.api_code == 187:
                    new_tweet = "RT " + tweet
                    if len(new_tweet) <= 277:
                        api.update_status("RT " + tweet)
                        tweeted.append(tweet)
                    else:
                        api.update_status("RT " + new_tweet[0:274])
                        tweeted.append(new_tweet)
                else:
                    continue
        else:
            continue
    else:
        api.update_status(tweet[0:279])
        tweeted.append(tweet[0:279])
        time.sleep(30)
        api.update_status(tweet[279:])
        tweeted.append(tweet[279:])

    time.sleep(600)
