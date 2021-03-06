# This will walk you through the process of creating your very own AI Twitter bot.

## Phase 1: Create a new Twitter account for the bot with developer access.

### Step 1: Create account.
This can be any Twitter account, or even your current one.

### Step 2: Apply for developer account access.
[Here is a link to do just that (you need to be signed in to the bot account already)](https://developer.twitter.com/en/apply-for-access).

### Step 3: Create a Twitter app in the bot's name. 
After getting approved for your developer account, you should be met with a page to create an application. 

Just in case, [here is a link to the page](https://developer.twitter.com/en/apps).

### Step 4: Acquire the access tokens. 
After creating the app, go to the Keys and tokens page to collect the `API key`, `Secret key` and generate the `Access token` and `Access token secret` keys. **Make sure to save them immediately, you have one chance to view them before they remain permanently hidden from view.** If you forget them you'll have to regenerate them.

## Phase 2: Download the target account's tweets into a CSV file.

### Step 1: Install the dependencies for Max Wolff's [python script.](https://github.com/minimaxir/download-tweets-ai-text-gen)

Enter `pip3 install twint==2.1.4 fire tqdm` into the command line of your system's Terminal, making sure you are in the same directory where the project is saved.

### Step 2: Download the tweets.

Run the command `python3 download_tweets.py <twitter_username>` where twitter_username is the @username of the Twitter account whose tweets you want to base the bot on. **It's *strongly advised* that you gain explicit permission before using this command on any account that you don't own.**

The more tweets you download, the more accurately the AI will parody your style. I reccommend at least 6000. If your account has fewer tweets than that, you will see less of the deviation from the source material that makes these parodies funny, and more verbatim tweets.

## Phase 3: Train the AI.

This bot uses a text-generating neural network known as [GPT2](https://openai.com/blog/better-language-models/).

You will have to train this AI using the CSV file that contains your tweets. 

### Step 1: Use Max Wolff's Google Colab Notebook to acquire the GPT2 AI.  
This [Google Colaboratory Notebook](https://colab.research.google.com/drive/1qxcQ2A1nNjFudAGN_mcMOnvV9sF_PkEb) contains *detailed* instructions on how exactly to do so. 

### Step 2: Train GPT2 using the CSV file of tweets you downloaded.
You will upload the CSV file to the Google Drive folder that the virtual machine within the notebook stores its data, then run the cell to begin the training based on that file. Instructions with details are on the notebook.

### Step 3: Create text files containing tweets generated by GPT2.
```
gen_file = 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.utcnow())

gpt2.generate_to_file(sess,
                      destination_path=gen_file,
                      length=200,
                      temperature=1.0,
                      top_p=0.9,
                      prefix='<|startoftext|>',
                      truncate='<|endoftext|>',
                      include_prefix=False,
                      nsamples=1000,
                      batch_size=20
                      )
```
You will run this cell to create .txt files containing 1000 [`nsamples`] tweets each, or however many tweets you wish each text file to hold. 

### Step 4
Download the text files from notebook and save them in this folder.

## Phase 4: Set up the server.

### Step 1: Store your access keys and tokens in `credentials.py`
Note that you'll be storing them in plaintext so do not show that file to anyone.

### Step 2: Install tweepy.
[Tweepy](http://docs.tweepy.org/en/v3.5.0/api.html) is the API that we will be using to actually tweet the tweets (Remember when we were supposed to be tweeting? Seems like ages ago, huh?)

* run the command `pip3 install setuptools` to acquire any miscellaneous dependencies.
* run the command `pip3 install tweepy` to acquire the tweepy API.

### Step 3: Tell the server where to tweet from.

In the line that says `filename = open('YOUR_TWEETS.txt','r')`, replace YOUR_TWEETS with the name of the text file that the GPT2 AI generated.

>Note that the tweets in these files will be delimited (separated) by `====================` on every new line after a tweet. This is what the line `bot_output = tweettext.split('====================')` is doing, separating each text file and storing the individual tweets as entries in the `bot_output` container.

### Step 4: Tell the server how often to tweet.

After all the error handling lines you will see a line at the very end: `time.sleep(600)`.

This line tells the server to wait for 600 seconds (ten minutes) before iterating through the `bot_output` container to bring up the next tweet. If this line wasn't here your bot would attempt to tweet as fast as your computer could compile the program. Twitter's API does not like that. 

**I would *highly* advise against making this bot tweet more frequently than every 90 seconds. One tweet every minute is pushing it.** 

An ideal frequency would be 2-5 minutes but 10 is often enough to be novel without becoming spam on people's timelines. But you're at the wheel.

### Step 4.5: Do your due diligence

**Before you start tweeting,** make sure that the bot's Twitter profile— which you should be logged in to, and have already given a username— makes the following *abundantly* clear, space on the bio allowing:

* That it’s posting AI-generated tweets.
* That those tweets are curated by you (or not curated by you)
* The Twitter account of who maintains the bot (should be your account)
* The Twitter account(s) the bot is parodying/based on. (should be accounts you have access to/permission to use for this)

**It should also very clearly indicate that it is not a real human being.** A username like 'PersonAI' or 'PersonBot' should do fine.

### Step 5: All systems go.

With that, you now have everything you need to get the bot up and running. 

Simply open your terminal, navigate to the project folder, and run the command `python3 server.py`.

Note that like with any program, this bot will need the server to keep running in order to be able to be 'live.' It's reccommended that you use an auxiliary computer solely dedicated to this, and not your primary computer that you use for other functions. You don't want too many processes competing with this.

### Step 5.5: Houston, we have a problem.

Barring a server collapse on Twitter's end, if your program crashes it's likely one of two errors occurred:

#### Error code 186: Duplicate Status.

Twitter doesn't let you tweet the same exact thing twice within a certain period of time. You shouldn't receive this error because the `tweeted` container handles it, but if you do, simply remove the offending tweet from the text file.

#### Error code 187: Limit Break.

Twitter doesn't let you tweet more than 280 characters. You also shouldn't receive this error because it's handled (twice) but if you do, simply add a `====================` between the offending tweet to space it out or remove it as you see fit.



## Appendix

You only need these first three starter files in the repo (plus any text file) to actually run the bot, but by the time you get to this part of the README you should have in your project directory the following files:

* server.py
* credentials.py
* download_tweets.py
* YourUsername_tweets.csv
* gpt2_gentext_YYYYMMDD_HHMMSS.txt (mulitple)

If you are missing one of these, you messed up somewhere, you should probably start over.

If you have any other questions about this or run into any issues, you can reach me on Twitter [@Paracelsus](https://twitter.com/Paracelsus).

A follow-up/update to this project would involve:

* Running it on a dedicated server such as a Raspberry Pi and the process involved with that.
* Storing multiple text files to read from, instead of manually replacing each one once the tweets are exhausted.
* Including images and videos with the tweets.


## Credits

download_tweets.py — [Max Wolff](https://github.com/minimaxir)

GPT2 Training Google Colaboratory Notebook — Max Wolff

server.py — Myself

credentials.py — Myself



## License

MIT
