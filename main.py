#Install the required Python libraries such as requests, BeautifulSoup, and SQLite3.
#pip install requests beautifulsoup4

#Importing the required libraries in Python.
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd
import sqlite3


#puting the URL of the website to scrape and send a request to fetch the HTML content.
url = 'https://www.theverge.com/'

response = requests.get(url)

#Parse the HTML content using BeautifulSoup and find the relevant elements such as headline, link, author, and date.
soup = BeautifulSoup(response.content, 'html.parser')


articles = soup.find_all('div', {'class': 'c-entry-box--compact__title'})

    
for article in articles:
    headline = article.find('a').get_text().strip()
    link = article.find('a')['href']
    author = article.find('span', {'class': 'c-byline__item'}).get_text().strip()
    date = datetime.now().strftime('%Y/%m/%d')
    articles.append((link, headline, author, date))
    
# saving data to csv file
filename = datetime.now().strftime('%d%m%Y_verge.csv')
df = pd.DataFrame(articles, columns=['URL', 'headline', 'author', 'date'])
df.index.name = 'id'
df.to_csv(filename)

conn = sqlite3.connect('verge_articles.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE articles
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              url TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

# Insert data into the table
for article in articles:
    c.execute("INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)",
              (article[0], article[1], article[2], article[3]))

# Commit changes and close connection
conn.commit()
conn.close()
