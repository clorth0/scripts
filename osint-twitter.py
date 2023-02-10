import tweepy

# Twitter API Auth
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")

# Create API object
api = tweepy.API(auth)

# Search for tweets containing the hashtag "#hacktheplanet"
tweets = tweepy.Cursor(api.search, q="#hacktheplanet").items(100)
for tweet in tweets:
    print(f"{tweet.user.name} said {tweet.text}")
