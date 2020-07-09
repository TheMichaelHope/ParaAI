import tweepy, time, random
from credentials import *
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) # these should be stored in credentials.py and passed in, do not copy paste them directly here
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET) # these should be stored in credentials.py and passed in, do not copy paste them directly here

api = tweepy.API(auth) # this line allows the twitter API access to your account: it can do a lot more than just tweet, read the documentation for more info

# open text file containing tweets and store its contents in tweettext
filename = open('batch_9.txt','r')
tweettext = filename.read()
filename.close()

# separate tweettext into its component tweets
bot_output = tweettext.split('====================')

# store already tweeted tweets in this container
tweeted = []


for tweet in bot_output:
    if len(tweet) <= 280: # error handling for Limit Break error (187)
        if tweet not in tweeted: # error handling for Duplicate error (186)
            try:
                api.update_status(tweet) # this is the line of code that actually sends tweets
                tweeted.append(tweet) # add tweet to tweeted container
            except tweepy.TweepError as error:
                # this section was my personalized solution to duplicate tweets, but you can simply discard it and leave the continue statement in place if you do not wish to see any duplicated tweets on this bot
                if error.api_code == 187:
                    new_tweet = "RT " + tweet
                    if len(new_tweet) <= 277:
                        api.update_status("RT " + tweet) # add RT to the tweet if it will keep it under 280
                        tweeted.append(tweet)
                    else:
                        api.update_status("RT " + new_tweet[0:274]) # cut off the last 3 characters to add RT
                        tweeted.append(new_tweet)
                elif error.api_code == 408:
                    new_tweet = "Links will be the death of me."
                    api.update_status(new_tweet)
                    tweeted.append(new_tweet)
                else:
                    continue
        else:
            continue
    else:
        # this section is my personalized solution to Limit Break tweets, simply splitting them up on the 280th character and tweeting them separately. You are free to choose another solution.
        api.update_status(tweet[0:279])
        tweeted.append(tweet[0:279])
        time.sleep(30)
        try:
            api.update_status(tweet[279:])
            tweeted.append(tweet[279:])
        except tweepy.TweepError as error:
            if error.api_code == 186:
                new_tweet = tweet[279:557]
                try:
                    api.update_status(new_tweet)
                    tweeted.append(new_tweet)
                except tweepy.TweepError as error:
                    if error.api_code == 186:
                        newer_tweet = new_tweet[0:279]
                        api.update_status(new_tweet)
                        tweeted.append(new_tweet)
                    elif error.api_code == 408:
                        new_tweet = "Links will be the death of me."
                        api.update_status(new_tweet)
                        tweeted.append(new_tweet)
                    else:
                        continue
            else:
                continue

    # this line tells the bot how often to tweet, in this default case every 600 seconds (10 mins)
    time.sleep(600) # I DO NOT RECCOMMEND PUTTING SMALLER NUMBER THAN 90 IN THIS LINE
