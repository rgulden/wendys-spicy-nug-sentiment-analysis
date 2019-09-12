import re
import got
from textblob import TextBlob 

# Scrub tweets of links, special characters and other junk.
def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Use textBlob to determine polarity.
def get_tweet_sentiment(tweet): 
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'

# Use got package to grab historical tweets
def get_tweets(query, since, until, count = 10): 
    # empty list to store parsed tweets 
    tweets = [] 

    # call twitter api to fetch tweets 
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(since).setUntil(until).setMaxTweets(count)

    # parsing tweets one by one 
    for tweet in got.manager.TweetManager.getTweets(tweetCriteria): 
        # empty dictionary to store required params of a tweet 
        parsed_tweet = {} 

        # saving text of tweet 
        parsed_tweet['text'] = tweet.text 
        # saving sentiment of tweet 
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text) 

        # appending parsed tweet to tweets list 
        if tweet.retweets > 0: 
            # if tweet has retweets, ensure that it is appended only once 
            if parsed_tweet not in tweets: 
                tweets.append(parsed_tweet) 
        else: 
            tweets.append(parsed_tweet) 

    # return parsed tweets 
    return tweets 
  
def main(): 
    # calling function to get tweets 
    tweets = get_tweets(query = 'wendys spicy nuggets', since = "2019-05-01", until = "2019-08-19", count = 1000)
    print("----Announcement to reveal----")
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
    
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text'])

    # calling function to get tweets 
    tweets = get_tweets(query = 'wendys spicy nuggets', since = "2019-08-20", until = "2019-09-09", count = 1000)
    print("----Reveal to current----")
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
    
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text'])

if __name__ == "__main__": 
    # calling main function 
    main() 