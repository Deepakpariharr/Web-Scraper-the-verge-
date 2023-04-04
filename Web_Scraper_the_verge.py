# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd
import sqlite3

# Defining the URL to scrape
url = 'https://www.theverge.com/'

# Defining the name of the database to use
dbname = 'verge_articles.db'

# Defining the name of the table to use
tablename = 'articles'

# Defining the name of the CSV file to use
csvname = 'verge.csv'

# Defining the function to get the articles
def getingArticles():
    # Sending a request to fetch the HTML content
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup and find the relevant elements
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles_divs = soup.find_all('div', {'class': 'c-entry-box--compact'})
    
    articles = []
    
    for article in articles_divs:
        # Geting the headline, link, author, and date of each article
        headline = article.find('meta', {'property': 'og:title'}).get('content')
        link = article.find('meta', {'property': 'og:url'}).get('content')
        author = article.find('meta', {'property': 'author'}).get('content')
        date = article.find('meta', {'property': 'article:published_time'}).get('content').split('T')[0]
        
        articles.append((link, headline, author, date))
    
    # Converting the list of articles into a pandas DataFrame
    df = pd.DataFrame(articles, columns=['url', 'headline', 'author', 'date'])
    
    # Droping any duplicate articles
    df = df.drop_duplicates()
    
    return df

# Defining the function to save the articles to a CSV file
def save_articles_into_csv(df):
    # Creating a filename based on the current date
    filename = datetime.now().strftime('%Y%m%d') + '_' + csvname
    
    # Saving the DataFrame to a CSV file
    df.to_csv(filename, index=False)

# Defining the function to save the articles to a SQL database
def save_articles_into_sql(df):
    # Creating a connection to the database
    conn = sqlite3.connect(dbname)
    
    # Checking if the table already exists
    if tablename in pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)['name'].tolist():
        # If the table already exists, deleting any articles that are already in the table
        df.to_sql(tablename, conn, if_exists='replace', index=False)
    else:
        # If the table does not exist, creating it and inserting the articles
        df.to_sql(tablename, conn, if_exists='append', index=False)
    
    # Closing the connection to the database
    conn.close()

# Geting the articles and save them to a CSV file and a SQL database
Articles_df = getingArticles()
save_articles_into_csv(Articles_df)
save_articles_into_sql(Articles_df)
