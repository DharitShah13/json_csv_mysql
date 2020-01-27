#! /usr/bin/env python3

import json
import oauth2 as oauth
import re
import configparser
import os
import sys

config = configparser.ConfigParser()
config.read('config.ini')

# connection tokens from config file
consumer_key = config.get('Tokens', 'consumer_key')
consumer_secret = config.get('Tokens', 'consumer_secret')
access_token_key = config.get('Tokens', 'access_token_key')
access_token_secret = config.get('Tokens', 'access_token_secret')

#Creating Client

consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
access_token = oauth.Token(key=access_token_key, secret=access_token_secret)
client = oauth.Client(consumer, access_token)

#tweets
screen_name = config.get('Tweet', 'screen_name')
tweet_count = config.get('Tweet', 'tweet_count')

#Search keword(s)
search_key = config.get('Search', 'search_keywords').replace(
    '#', '%23').replace(' ', '%20').lower()
search_count = config.get('Search', 'search_count')


# json file, directory
dir = os.getcwd()
json_file = config.get('Json', 'File_Name')


def getTweets(screen_name, tweet_count, json_file):
    user_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=' + \
        screen_name + '&count=' + str(tweet_count) + '&tweet_mode=extended'
    print(user_url)
    response, t = client.request(user_url)
    tweet_data = json.loads(t)

    try:
        if tweet_data[1]:
            with open(json_file, 'w') as f:
                json.dump(tweet_data, f)
            print("Created a Json \nfile: " +
                  json_file + "\ndirectory: " + dir)
            print("------------------------------------------------")
    except KeyError:
        try:
            print(tweet_data['errors'][0]['message'] + "\nTokens Used:\n" + "consumer_key=" + consumer_key +
                  "\nconsumer_secret=" + consumer_secret +
                  "\nccess_token_key=" + access_token_key +
                  "\nccess_token_secret=" + access_token_secret +
                  "\n\nExiting the script")
            sys.exit()
        except KeyError:
            print("User " + screen_name + " is " +
                  tweet_data['error'].lower() + " from your account")
            sys.exit()


def getHashtags(search, count):

    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + search +\
        "&count=" + str(count) + \
        "&result_type=recent&tweet_mode=extended"

    response, x = client.request(url)
    hashtag_data = json.loads(x)
    hashtags_regex = re.compile(r'#\S+')

    hashtags_list = []
    for row in hashtag_data['statuses']:
        try:
            hashtags_list.extend(hashtags_regex.findall(
                row['retweeted_status']['full_text'].lower()))
        except KeyError:
            hashtags_list.extend(
                hashtags_regex.findall(row['full_text'].lower()))

    hashtags_cnt = {}
    for hashtag in hashtags_list:
        try:
            hashtags_cnt[hashtag] += 1
        except KeyError:
            hashtags_cnt[hashtag] = 1
    print("Hashtags used in the search ordered by count:")
    for k, v in sorted(hashtags_cnt.items(), key=lambda x: x[1], reverse=True):
        print("Hashtag: %s, Count: %d" % (k, v))


if __name__ == '__main__':

    getTweets(screen_name, tweet_count, json_file)
    getHashtags(search_key, search_count)
