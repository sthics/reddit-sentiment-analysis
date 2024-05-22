import praw
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk

# Install required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Reddit API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
user_agent = 'your_user_agent'

# Initialize the Reddit API client
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Function to fetch data from a subreddit
def fetch_reddit_data(subreddit, limit=100):
    subreddit = reddit.subreddit(subreddit)
    posts = []
    for post in subreddit.hot(limit=limit):
        posts.append([post.title, post.selftext, post.score, post.num_comments, post.created_utc])
    return pd.DataFrame(posts, columns=['Title', 'Text', 'Score', 'Comments', 'Created_At'])

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+|@\S+|\n', '', text)
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.lower() not in stopwords.words('english')]
    return ' '.join(tokens)

# Function to get sentiment
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Fetch and preprocess data
subreddit_data = fetch_reddit_data('learnpython', limit=100)
subreddit_data['Processed_Text'] = subreddit_data['Title'] + ' ' + subreddit_data['Text']
subreddit_data['Processed_Text'] = subreddit_data['Processed_Text'].apply(preprocess_text)
subreddit_data['Sentiment'] = subreddit_data['Processed_Text'].apply(get_sentiment)

# Plot the sentiment distribution
sentiment_counts = subreddit_data['Sentiment'].value_counts()
plt.figure(figsize=(8, 6))
sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title('Sentiment Analysis of Reddit Posts')
plt.xlabel('Sentiment')
plt.ylabel('Number of Posts')
plt.show()
