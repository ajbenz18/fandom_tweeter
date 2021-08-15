import tweepy
import yaml
import random
import sys

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

        self.auto_retweet()

        self.auto_reply()

    def auto_retweet(self):
        '''
        Performs action of finding a popular tweet, then retweets it
        '''
        # list of possible topics. Some are listed twice for higher weighting
        possible_topics = ['nfl', 'nfl', 'nfl', 'nba', 'nba', 'nba', 'college football', 'college football', 'college basketball', 'mlb', 'premier league', 'nhl']
        topic = random.choice(possible_topics)

        possible_tweets = self.api.search(topic, result_type='popular', count=10)

        highest_score = 0 # (likes + retweets) / number of followers
        highest_score_index = 0
        for i, t in enumerate(possible_tweets):
            if not self.is_viable(t, follower_threshold_low=1000):
                continue # prevent division by 0
            score = (t.retweet_count + t.favorite_count) / t.user.followers_count
            if score > highest_score: # track the most well-liked tweet
                highest_score = score
                highest_score_index = i

        if highest_score_index >= 0: # make sure we found a viable tweet to retweet
            self.api.retweet(possible_tweets[highest_score_index].id)
            print(f"Retweeted {possible_tweets[highest_score_index].text} from {possible_tweets[highest_score_index].author.name}")
        else:
            print('Found no good tweets to retweet')

    def auto_reply(self):
        '''
        performs action of selecting a topic, finding a tweet about it, and replying to it
        '''
        # choose topic
        topic = self.select_reply_topic()

        # reply to the tweet
        original_tweet = self.find_tweet(topic)

        # reply to the tweet
        post = self.reply(original_tweet, topic)

    def select_reply_topic(self):
        '''
        Opens the responses.yaml file and randomly selects a top to tweet about
        '''
        with open('responses.yaml', 'r') as stream:
            self.topic_tweet_choices = yaml.load(stream)
        topic = random.choice(list(self.topic_tweet_choices.keys()))
        return topic

    def is_viable(self, tweet, follower_threshold_low=-sys.maxsize-1, follower_threshold_high=sys.maxsize):
        '''
        checks if the given tweet meets our criteria for tweets we want to reply to
        Tweeter must have less followers tha upper threshold and more than lower threshold
        Tweet must not be a reply
        Tweet must not be a retweet
        '''
        print(tweet.author.followers_count)
        if tweet.author.followers_count > follower_threshold_high or tweet.author.followers_count < follower_threshold_low:
            return False
        if tweet.in_reply_to_screen_name: # can not be a reply
            return False
        if tweet.is_quote_status: # cannot be retweet
            return False
        return True

    def find_tweet(self, topic):
        '''
        Finds tweet to reply to about the given topic
        '''
        tweets = self.api.search(topic, result_type='recent', count=12)
        choice = None
        for t in tweets:
            if self.is_viable(t, follower_threshold_high=10000):
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
        if media_path != "": # if we have an image or GIF to upload
            media = self.api.media_upload(media_path)
            post = self.api.update_status(message, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True, media_ids=[media.media_id])
            return post
        else: # if we don't have an image or GIF to upload
            post = self.api.update_status(message, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True)
            return post
        

        
        