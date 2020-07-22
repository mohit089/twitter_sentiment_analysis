import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    #This will authenticate twitter account, in this its using Sahil Tekwani's twitter account\
    #Each account has a unique consumerKey, consumerSecret, consumerToken, consumerSecretToken
    #These keys are obtained after making a regular twitter account as a developer account.
    #Entire authentication process in a function of tweepy library
    def DownloadData(self):
        consumerKey = "PqV21kbup2PYMZrRmfQxBjXSK"
        consumerSecret = "JFmOFJaLWN9qUoTknLrzqLKtyB6tishMCY35cIL423EoTJZfy7"
        accessToken = "1361593146-xydgaL52KVlLS1Aye4KjKoMHk4eTuGee0PVnLEl"
        accessTokenSecret = "snZyKFWSsSq8npWX6kMC23Vol07yBlFBaYU9PQ1pDRpo9"
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        #This will search for tweets
        #It will search a number of tweets based on 'NoOfTerms' entered by the user. 
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        csvFile=open('result.csv','w+')
        csvWriter=csv.writer(csvFile)    
        # creating variables to store info
        polarity = 0 #avg polarity variable
        positive = 0 #positive polarity variable
        negative = 0 #negative polarity variable
        neutral = 0 #neutral polarity variable


        # iterating through tweets fetched and adding them to get the reaction average later
        # analysis.sentiment.polarity is a funtion of textblob library which will analyse the sentiment and return -1,0 or +1
        # -1 is negative sentiment
        # 0 is neutral
        # +1 is positive sentiment
        
        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity  

            if (analysis.sentiment.polarity == 0):
                neutral += 1
          
            elif (analysis.sentiment.polarity > 0.00 and analysis.sentiment.polarity <= 1.00):
                positive += 1
          
            elif (analysis.sentiment.polarity > -1.00 and analysis.sentiment.polarity <= -0.1):
                negative += 1

        csvWriter.writerow(self.tweetText)
        csvFile.close()
        # finding average of how people are reacting based on tweets
        #print(positive,negative,neutral)
        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        #print("Average Polarity "+str(polarity))
        print("General Report: ")
        exp1=0
        exp2=0
        exp3=0
        if (neutral > negative and neutral > positive):
            print("Neutral")
            exp1=0.2
        elif (positive > neutral and positive > negative):
            print("Positive")
            exp2=0.2
        #elif (polarity > -1.00 and polarity <= -0.1):
        elif (negative > positive and negative > neutral):
            print("Negative")
            exp3=0.2
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)
        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

        #plotting pie chart 
        self.plotPieChart(positive, negative, neutral, searchTerm, NoOfTerms,exp1,exp2,exp3)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet using regular expression
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms,exp1,exp2,exp3):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['green','yellow','red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90,shadow="True",explode=[exp2,exp1,exp3])
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

#this is main function here we are calling sentiment analysis class created above

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
