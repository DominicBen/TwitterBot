#Main.py
#Currently takes username input from standard in, and loads a number of their most recent tweets
#compiles tweets into tweet and word lists



import requests
from requests_oauthlib import OAuth1Session
import os
import re
import json

#Keys
bearer_token = "AAAAAAAAAAAAAAAAAAAAANFZkAEAAAAAcbt4rpBeyGu7XabbkE5ELZCls1U%3DCKenkgVxCDZOIqdUfPwKZ0PLeR4Aa88IeLMCUcAwFbBpmK2ILC"
consumer_key="zVRFEdqda40gCSYhgNvaFsczj"
consumer_secret="aAihYDq9BLPQOHaZqPpiMZTJaZlGQ7Sr3f313cUFPJuCVHxVWj"
access_token="2740386898-WuFjk0S78QG53MeLJOjEMD6hOT9UsTxRd8WLAxd"
access_token_secret="PGjsaILf0eZweNXQkcpym0D0Mlrw6Hw2aPztghkXscmEm"


#process text of tweet
def process_tweet(text):
  text = re.sub(r'\.', ' . ', text)
  text = re.sub(r',', ' , ', text)
  text = re.sub(r';', ' ; ', text)
  # text = re.sub(r':', ' : ', text)
  text = re.sub(r'!', ' ! ', text)
  text = re.sub(r'\?', ' ? ', text)
  text = re.sub(r'\(', ' ( ', text)
  text = re.sub(r'\)', ' ) ', text)
  text = re.sub(r'"', ' " ', text)
  # text = re.sub(r"'", " ' ", text)
  

  text = re.sub(r' +', ' ', text)


  text = re.sub(r'&lt;', '<', text)
  text = re.sub(r'&gt;', '>', text)
  text = re.sub(r'&amp;', '&', text)

  return(text)


def bearer_oauth(r):
  """
  Method required by bearer token authentication.
  """

  r.headers["Authorization"] = f"Bearer {bearer_token}"
  r.headers["User-Agent"] = "rnntweet-generator"
  return r

#need to get user id for this to work
def get_user_data(username):
  usernames = f"usernames={username}"
  user_fields = "user.fields=description,created_at"

  #Formulate query by url to search for particular user data
  url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)

  #execute request
  response = requests.request("GET", url, auth=bearer_oauth,)
  # print(response.status_code)
  if response.status_code != 200:
    raise Exception(
      "Request returned an error: {} {}".format(
        response.status_code, response.text
      )
    )
  
  return response.json()

def fetch_tweets(url, params):
  response = requests.get(url, auth=bearer_oauth, params=params)
  # print(response.status_code)
  if response.status_code != 200:
      raise Exception(response.status_code, response.text)
  return response.json()



def grab(username, numoftweets):

  #get the user id for tweet request
  user_data = get_user_data(username)
  user_id = user_data['data'][0]['id']

  #search url that all of the tweet requests will use
  search_url = search_url = f'https://api.twitter.com/2/users/{user_id}/tweets'

  query_params = {'tweet.fields' : 'text', 'exclude' : 'retweets,replies', 'max_results' : '10'}

  number_of_tweets = numoftweets

  response = fetch_tweets(search_url, query_params)
  
  # print(json.dumps(response, indent=4, sort_keys=True))
  next_token = response['meta']['next_token']
  fetched_tweets = 0
  tweet_list = []
  word_list = []


  while fetched_tweets < number_of_tweets:
    temp_fetched_tweets = int(response['meta']['result_count'])

    for tweet in response['data']:
      text = tweet['text']

      #don't include tweets with images or links
      if 'https:' not in text:
        fetched_tweets = fetched_tweets + 1
        data = process_tweet(text)
        # print(data)

        if tweet not in tweet_list:
          #if tweet has not already been added to environment
          tweet_list.append(data)
          for word in data.split(' '):
            if word not in word_list:
              word_list.append(word)



    query_params = {'tweet.fields' : 'text', 'exclude' : 'retweets,replies', 'max_results' : '10', 'pagination_token' : next_token}
    response = fetch_tweets(search_url, query_params)
    next_token = response['meta']['next_token']

  #word list contained in word_list
  #tweets contained in tweet_list
  #tweets already formatted so they can be directly mapped into input with split(' ')
  #treating punctuation as a 'word' internally currently. We should discuss implications of this
  #formatting means that after result is generated we'll need to remove some of the buffered spaces added between punctuation and words
  print(word_list)
  print(tweet_list)
  return word_list