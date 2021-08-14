import tweepy
import yaml
import random

class System():
    '''
    System class to control application
    '''
    def __init__(self):
        '''
        Constructor
        Sets up API connection
        '''
        with open('keys.yaml', 'r') as stream:
            keys = yaml.load(stream)
        consumer_key = keys['api_key']
        consumer_secret = keys['api_secret_key']
        access_token = keys['access_token']
        access_token_secret = keys['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

        # choose topic
        topic = self.select_topic()

        # reply to the tweet
        original_tweet = self.find_tweet(topic)

        # reply to the tweet
        post = self.reply(original_tweet, topic)

    def select_topic(self):
        '''
        Opens the responses.yaml file and randomly selects a top to tweet about
        '''
        with open('responses.yaml', 'r') as stream:
            self.topic_tweet_choices = yaml.load(stream)
        topic = random.choice(list(self.topic_tweet_choices.keys()))
        return topic

    def is_viable(self, tweet):
        '''
        checks if the given tweet meets our criteria for tweets we want to reply to'''
        print(tweet.author.followers_count)
        if tweet.author.followers_count > 10000:
            print("here")
            return False
        if tweet.in_reply_to_screen_name:
            return False
        if tweet.is_quote_status:
            return False
        return True

    def find_tweet(self, topic):
        '''
        Finds tweet to reply to about the given topic
        '''
        tweets = self.api.search(topic, result_type='recent', count=12)
        choice = None
        for t in tweets:
            if self.is_viable(t):
                choice = t 
                break
        return choice

    def reply(self, original_tweet, topic):
        '''
        Builds tweet using information in the responses.yaml file and then tweets it back at original post
        '''
        if original_tweet is None:
            return

        tweet_choices = self.topic_tweet_choices[topic]
        response_number = random.choice(list(tweet_choices.keys()))
        post_info = tweet_choices[response_number]
        message = post_info['tweet']
        media_path = post_info['media']
        if media_path != "":
            media = self.api.media_upload(media_path)
            post = self.api.update_status(message, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True, media_ids=[media.media_id])
            return post
        else:
            post = self.api.update_status(message, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True)
            return post


        

        
        