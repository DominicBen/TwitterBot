
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



def grabdataset(username, numoftweets):
  username = input()

  #total number of tweets being fetched
  number_of_tweets = numoftweets

  dataset = "../datasets/tweet_list.txt"
  data_file = open(dataset, 'r')

  sample_tweet = data_file.readline()
  if sample_tweet == "":
    sample_tweet = data_file.readline()

  training_tweet_list = []
  training_word_list = []
  training_tweet_list1d = []

  while sample_tweet != "":
    formatted_tweet = process_tweet(sample_tweet)
    # print(data)

    if formatted_tweet not in training_tweet_list:
      #if tweet has not already been added to environment
      training_tweet_list.append(formatted_tweet)
      contains_link = False
      for word in formatted_tweet.split(' '):
        if 'http' not in word:
          if (contains_link == False) and (word not in training_word_list): 
            training_word_list.append(word)
        else:
          contains_link = True #if image or link is in the tweet, drop the rest of the link
      # print(formatted_tweet)

    sample_tweet = data_file.readline()
    if sample_tweet == "":#allow for a single empty line to appear without breaking input
      sample_tweet = data_file.readline()


  #get the user id for tweet request
  user_data = get_user_data(username)
  user_id = user_data['data'][0]['id']

  #search url that all of the tweet requests will use
  search_url = search_url = f'https://api.twitter.com/2/users/{user_id}/tweets'

  query_params = {'tweet.fields' : 'text', 'exclude' : 'retweets,replies', 'max_results' : '10'}


  response = fetch_tweets(search_url, query_params)
  
  # print(json.dumps(response, indent=4, sort_keys=True))
  next_token = response['meta']['next_token']#this in an indexing variable so that the request can be repeated to scan through more tweets
  fetched_tweets = 0
  tweet_list = []
  # word_list = []


  while fetched_tweets < number_of_tweets:
    temp_fetched_tweets = int(response['meta']['result_count'])

    for tweet in response['data']:
      text = tweet['text']

      
      data = process_tweet(text)
      # print(data)

      if tweet not in tweet_list:
        #if tweet has not already been added to environment
        tweet_list.append(data)
        for word in data.split(' '):
          if word not in training_word_list:
            if 'http' not in word:#don't include images or links
              fetched_tweets = fetched_tweets + 1
              training_word_list.append(word)



    query_params = {'tweet.fields' : 'text', 'exclude' : 'retweets,replies', 'max_results' : '10', 'pagination_token' : next_token}
    response = fetch_tweets(search_url, query_params)
    next_token = response['meta']['next_token']

  for tweet in training_tweet_list:
    temp = tweet.split(' ')
    training_tweet_list1d = training_tweet_list1d + temp

  print(training_tweet_list1d) 

  return training_tweet_list1d
  print(f'Training set: {len(training_tweet_list)} tweets')
  print(f'Number of unique words: {len(training_word_list)}')

