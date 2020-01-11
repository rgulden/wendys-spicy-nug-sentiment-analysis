import re, arrow
from TweetManager import TweetManager
from textblob import TextBlob
from threading import Thread, Event
from queue import Queue
from datetime import date, timedelta

dates = Queue()
tweets_w_polarity = Queue()


class Tweet_Worker(Thread):
    def run(self):
        while True:

            # this will return aclear date in format 2019-00-00
            # Get day
            key = dates.get()
            # Get day until (day + 1)
            day = arrow.get(key, "YYYY-MM-DD").date() + timedelta(days=1)

            tweets_w_polarity.put(
                get_tweets(
                    query="wendys spicy nuggets", since=key, until=str(day), count=100
                )
            )

            dates.task_done()


# Scrub tweets of links, special characters and other junk.
def clean_tweet(tweet):
    return " ".join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()
    )


# Use textBlob to determine polarity.


def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


# Use got package to grab historical tweets


def get_tweets(query, since, until, count=10):
    # empty list to store parsed tweets
    tweets = []

    # call twitter api to fetch tweets
    Tweeter = TweetManager()
    Tweeter.setQuerySearch(query)
    Tweeter.setSince(since)
    Tweeter.setUntil(until)
    Tweeter.setMaxTweets(count)

    # parsing tweets one by one
    for tweet in Tweeter.getTweets():
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}

        # saving text of tweet
        parsed_tweet["text"] = tweet["text"]
        # saving sentiment of tweet
        parsed_tweet["sentiment"] = get_tweet_sentiment(tweet["text"])

        # appending parsed tweet to tweets list
        if tweet["retweets"] > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)

    # return parsed tweets
    return tweets


def populate_queue_before():

    sdate = date(2019, 5, 4)  # start date
    edate = date(2019, 8, 17)  # end date

    delta = edate - sdate  # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.put(str(day))


def populate_queue_after():

    sdate = date(2019, 8, 21)  # start date
    edate = date(2019, 9, 11)  # end date

    delta = edate - sdate  # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.put(str(day))


def main():

    # populate queue with Dates
    populate_queue_before()

    # Create threads once queue is full
    for i in range(100):
        print("-", end="")
        t = Tweet_Worker()
        t.daemon = True
        t.start()

    # Wait for threads to finish
    dates.join()

    # For each tweet array in queue combine to one giant array
    tweets = []
    while not tweets_w_polarity.empty():
        tweets = tweets + tweets_w_polarity.get()

    # Output results
    print("----Announcement to reveal----")
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet["sentiment"] == "positive"]
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet["sentiment"] == "negative"]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print(
        "Neutral tweets percentage: {} %".format(
            100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
        )
    )

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet["text"])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet["text"])

    # populate queue with Dates
    populate_queue_after()

    # Wait for threads to finish
    dates.join()

    # For each tweet array in queue combine to one giant array
    tweets = []
    while not tweets_w_polarity.empty():
        tweets = tweets + tweets_w_polarity.get()

    # calling function to get tweets
    tweets = get_tweets(
        query="wendys spicy nuggets", since="2019-08-20", until="2019-09-09", count=100
    )
    print("----Reveal to current----")
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet["sentiment"] == "positive"]
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet["sentiment"] == "negative"]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print(
        "Neutral tweets percentage: {} %".format(
            100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
        )
    )

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet["text"])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet["text"])


if __name__ == "__main__":
    # calling main function
    main()
