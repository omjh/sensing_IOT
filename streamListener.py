#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sched
import time
import csv

#Variables that contains the user credentials to access Twitter API
access_token = "1213514274397536256-20fRqtzrbWDhzcodupEqyIyl4N0bjp"
access_token_secret = "9xKbJJNYU8eKHDUuxCRHGLp4hAOnJqB7jAgosWogNzRUl"
consumer_key = "Tcp3o0qG1KJRB26kpmioj4dGx"
consumer_secret = "c6ZoFisDsuHMF9wCkPo7lKfAbRMuEsbm92xLPkRjT9VztxADZc"

def freq_counter_file_creator():
    # create filename at the time the program started running
    fqfile = 'Frequency_file.csv'
    csvfqFile = open(fqfile, 'w')
    csvfqWriter = csv.writer(csvfqFile)
    csvfqWriter.writerow(['Time', 'Frequency'])
    return fqfile

def do_something(sc,l,fqfile):
    #open csv
    csvfqFile = open(fqfile, 'a')
    csvfqWriter = csv.writer(csvfqFile)

    #write csv
    print(l.count)
    csvfqWriter.writerow([time.strftime('%Y%m%d-%H%M%S'), l.count])
    #reset counter
    l.count = 0
    s.enter(60, 1, do_something, (sc,l, fqfile))

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    #Add Count

    def __init__(self, api = None):
        #API stuff
        self.api = api
        #count
        self.count = 0
        #used to limit tweet data
        self.counter = 0
        #create filename at the time the program started running
        self.filename = 'Microsoft_'+time.strftime('%Y%m%d-%H%M%S')+'.csv'
        csvFile = open(self.filename, 'w')
        #create writer
        csvWriter = csv.writer(csvFile)
        #Headers in CSV file
        csvWriter.writerow(['Created at', 'text', 'Re-tweet Count'])


    def on_status(self, status):

        csvFile = open(self.filename, 'a')
        csvWriter = csv.writer(csvFile)

        #Counter
        self.count += 1
        #print(self.count)
        #Added to deal with emojis and fonts that cant be encoded by the csvwrite function.
        #These tweets are stored just for visualisation purposes later.
        if self.count < 2:
            try:
                csvWriter.writerow([status.created_at,status.text,status.retweet_count])
            except UnicodeEncodeError:
                csvWriter.writerow([status.created_at,'Unicode Error',status.retweet_count])
        return True

    def on_error(self, status_code):
        print(status_code)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['Microsoft','microsoft'], is_async=True)
    print('---Running Twitter Listener for Microsoft---')
    filename = freq_counter_file_creator()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(60, 1, do_something, (s,l,filename))
    s.run()
