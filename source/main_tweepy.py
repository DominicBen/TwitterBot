#gets tweets from twitter for a particular user
import tweepy

#Keys
bearer_key = "AAAAAAAAAAAAAAAAAAAAANFZkAEAAAAAcbt4rpBeyGu7XabbkE5ELZCls1U%3DCKenkgVxCDZOIqdUfPwKZ0PLeR4Aa88IeLMCUcAwFbBpmK2ILC"
consumer_key="zVRFEdqda40gCSYhgNvaFsczj"
consumer_secret="aAihYDq9BLPQOHaZqPpiMZTJaZlGQ7Sr3f313cUFPJuCVHxVWj"
access_token="2740386898-WuFjk0S78QG53MeLJOjEMD6hOT9UsTxRd8WLAxd"
access_token_secret="PGjsaILf0eZweNXQkcpym0D0Mlrw6Hw2aPztghkXscmEm"


#Initialize client requesting permissions
client = tweepy.Client(bearer_key)

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# auth = tweepy.OAuth2AppHandler(
#     consumer_key=consumer_key, consumer_secret=consumer_secret
# )
# api = tweepy.API(auth)

#currently this request gets denied
#working on it
public_tweets = client.get_users_tweets(id = "AndyOnTheNet")
for tweet in public_tweets:
    print(tweet.text)



