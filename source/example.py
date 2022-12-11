import requests
from requests_oauthlib import OAuth1Session
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAANFZkAEAAAAAcbt4rpBeyGu7XabbkE5ELZCls1U%3DCKenkgVxCDZOIqdUfPwKZ0PLeR4Aa88IeLMCUcAwFbBpmK2ILC"

consumer_key="zVRFEdqda40gCSYhgNvaFsczj"
consumer_secret="aAihYDq9BLPQOHaZqPpiMZTJaZlGQ7Sr3f313cUFPJuCVHxVWj"

# search_url = "https://api.twitter.com/2/tweets/search/all"

# usernames = "usernames=AndyOnTheNet"
# username_search_url = f"https://api.twitter.com/2/users/by?{usernames}"

def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=AndyOnTheNet"
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

username_search_url = create_url()

# username_search_url = "https://api.twitter.com/2/users/by/username/:AndyOnTheNet"

# request_token_url = "https://api.twitter.com/oauth/request_token"
# oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# try:
#     fetch_response = oauth.fetch_request_token(request_token_url)
# except ValueError:
#     print(
#         "There may have been an issue with the consumer_key or consumer_secret you entered."
#     )

# resource_owner_key = fetch_response.get("oauth_token")
# resource_owner_secret = fetch_response.get("oauth_token_secret")
# print("Got OAuth token: %s" % resource_owner_key)

# base_authorization_url = "https://api.twitter.com/oauth/authorize"
# authorization_url = oauth.authorization_url(base_authorization_url)
# print("Please go here and authorize: %s" % authorization_url)
# verifier = input("Paste the PIN here: ")

# Get the access token
# access_token_url = "https://api.twitter.com/oauth/access_token"
# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=resource_owner_key,
#     resource_owner_secret=resource_owner_secret,
#     verifier=verifier,
# )
# oauth_tokens = oauth.fetch_access_token(access_token_url)

# access_token = oauth_tokens["oauth_token"]
# access_token_secret = oauth_tokens["oauth_token_secret"]

# # Make the request
# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=access_token,
#     resource_owner_secret=access_token_secret,
# )



# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'tweet.fields' : 'text', 'exclude' : 'retweets,replies'}
# query_params = {'query': '(from:AndyOnTheNet -is:retweet -is:reply)','tweet.fields': 'author_id', 'max_results' : '10'}



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "rnntweet-generator"
    return r


def get_user_data(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

# def lookup_user_id(url, username):
#     response = requests.request("GET", url, auth=bearer_oauth,)
#     print(json.dumps(response, indent=4, sort_keys=True))
#     print(response['data']['id'])
#     return(response['data']['id'])


def connect_to_endpoint(url, params):

    user_search_url = create_url()
    user_response = get_user_data(user_search_url)
    # print(json.dumps(user_response['data'][0]['id'], indent=4, sort_keys=True))
    user_id = user_response['data'][0]['id']
    search_url = f'https://api.twitter.com/2/users/{user_id}/tweets'

    response = requests.get(search_url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    search_url = "https://api.twitter.com/2/tweets/search/all"
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()