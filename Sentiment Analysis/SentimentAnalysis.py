import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
import pyodbc

#This is a mulitiline string
connection = (

    "Driver={SQL Server};"
    "Server=MUKTA\\SQLEXPRESS;"  #I need to put one extra slash
    "Database=PortfolioProject_MarketingAnalytics;"
    "Trusted_Connection=yes;"

)




# Connecting to the database
conn = pyodbc.connect(connection)

query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating,REPLACE(ReviewText, '  ', ' ') as ReviewText FROM customer_reviews"

df = pd.read_sql(query,conn)

# Function to define the sentiment category based on the sentiment analysis score and customer rating.
def category_sentiment(score, rating):
    if score >= 0.05:
        if rating >3:
            return 'Positive'
        elif rating ==3:
            return 'Mixed Positive'
        else:
            return 'Mixed Negative'
        
    elif score <= -0.05 :
        if rating >3:
            return 'Mixed Positive'
        elif rating ==3:
            return 'Mixed negative'
        else:
            return 'Negative'
        
    else:
        if rating >3:
            return 'Positive'
        elif rating ==3:
            return 'Neutral'
        else:
            return 'Negative'
        

# Function to define sentiment buckets based on the sentiment analysis scores.
def sentiment_bucket(score):
    # Positive
    if score>= 0.5:
        return '[0.5 , 1]'  
    # Negative
    elif score <= -0.5:
        return '[-1, -0.5]'
    # Mildly Negative
    elif score > -0.5 and score < 0:
        return '(-0.5,0)'
    # Mildly Positive
    else:
        return '[0, 0.5)'
    


df["Review_Scores"] = df['ReviewText'].apply(lambda x : sia.polarity_scores(x)['compound'])
        
df['SentimentCategory'] = df.apply(lambda x : category_sentiment(x["Review_Scores"], x["Rating"]), axis =1)
    
df['SentimentBucket'] = df['Review_Scores'].apply(lambda x : sentiment_bucket(x) )

df.to_csv('fact_customer_reviews_with_sentiment.csv' , index = False)

