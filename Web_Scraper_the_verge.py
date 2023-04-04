# Install the required Python libraries
# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd
import sqlite3

# Putting the URL of the website to scrape and sending a request to fetch the HTML content.
url = 'https://www.theverge.com/'

response = requests.get(url)

# Parse the HTML content using BeautifulSoup and find the  headline, link, author, and date.
soup = BeautifulSoup(response.content, 'html.parser')

articles_divs = soup.find_all('div', {'class': 'c-entry-box--compact'})

articles = []

for article in articles_divs:
    headline = article.find('meta', {'property': 'og:title'}).get('content')
    link = article.find('meta', {'property': 'og:url'}).get('content')
    author = article.find('meta', {'property': 'author'}).get('content')
    date = article.find('meta', {'property': 'article:published_time'}).get('content').split('T')[0]
    articles.append((link, headline, author, date))
    
    print(f"Link: {link}")
    print(f"Headline: {headline}")
    print(f"Author: {author}")
    print(f"Date: {date}")

# saving data to csv file
filename = datetime.now().strftime('%d%m%Y_verge.csv')
df = pd.DataFrame(articles, columns=['URL', 'headline', 'author', 'date'])
df.index.name = 'id'
df.to_csv(filename)

# Creating and connecting to a SQLite3 database and insert data into it
conn = sqlite3.connect('verge_articles.db')
c = conn.cursor()

# Creating table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              url TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

# Inserting data into the table
for article in articles:
    c.execute("INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)",
              (article[0], article[1], article[2], article[3]))

# Commit changes and close connection
conn.commit()
conn.close()
