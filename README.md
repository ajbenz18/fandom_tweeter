# fandom_tweeter
A twitter bot that runs the account @5portball

## What it does
fandom_tweeter does two things: Retweet popular sports-related tweets and reply to sports related tweets about specific tops

### Retweeting
The program has a set of topics that it searches for popular tweets in, and then chooses to retweet the one with the highest ratio of likes and retweets to followers.

### Replying
```responses.yaml``` contains a variety of my own sports takes/jokes on several different sports topics. The program chooses ones of those topics at random and finds a tweet about that topic. It then replies to the tweet with one of the prewritten responses to that topic.

## How it works
fandom_tweeter uses the Twitter API and tweepy Python library to post and search for tweets. It runs daily on an AWS Lambda function.
