import os
import tweepy

client = tweepy.Client(
    bearer_token=os.environ.get("BEARER_TOKEN"),
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token=os.environ["ACCESS_KEY"],
    access_token_secret=os.environ["ACCESS_SECRET"],
)

SEARCH_QUERY = os.environ.get("SEARCH_QUERY", "Python -is:retweet lang:ja")
MAX_RESULTS = int(os.environ.get("MAX_RESULTS", "10"))

response = client.search_recent_tweets(
    query=SEARCH_QUERY,
    max_results=MAX_RESULTS,
    tweet_fields=["created_at", "author_id", "text"],
)

if not response.data:
    print("No tweets found.")
else:
    print(f"Query: {SEARCH_QUERY}")
    print(f"Found: {len(response.data)} tweets\n")
    for tweet in response.data:
        print(f"[{tweet.created_at}] {tweet.author_id}")
        print(f"  {tweet.text}")
        print()
