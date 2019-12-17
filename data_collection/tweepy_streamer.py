'''
 This program is updated in such a way that it can collect and store twitter data up to a predefined MAX_TWEETS_COUNT in a file.
 In each run, a new output file is generated with file_YYYYMMDDHHMMSS.txt 
 
 Mehmet Acikgoz, December 2019
 
'''

# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime

import sys  
import twitter_credentials
 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)
        


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    counter = 0
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        if StdOutListener.counter == MAX_TWEETS_COUNT :
            sys.exit("Tweets are stored")
        try:
            #print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            StdOutListener.counter += 1
            if StdOutListener.counter % (MAX_TWEETS_COUNT/100) == 0:
               print(StdOutListener.counter)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
    # to create the filename for file.inp
    now = str(datetime. now()).replace(' ' , '').replace('-','').replace(':','')
    filename = 'file_'+now[0:now.find('.')]+'.txt'
    fid= open("file.inp","w")
    fid.write(filename)
    fid.close()
    
    
    MAX_TWEETS_COUNT = 100
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    #hash_tag_list = ["donal trump", "hillary clinton", "barack obama", "bernie sanders"]        
    # hash_tag_list = []    
    fetched_tweets_filename = filename

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
