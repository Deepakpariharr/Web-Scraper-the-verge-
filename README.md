## Web-Scraper-the-verge-
#Read the headline, get the link of the article, the author, and the date of each of the articles
found on "theverge.com"
- Storing these in a CSV file titled `ddmmyyy_verge.csv`, with the following header `id, URL,
headline, author, date`.
- Creating an SQLite database to store the same data, and make sure that the id is the primary
key

- Saving the articles (and de-duplicating them) daily on the server in a SQL Database.


This code defines three functions: getArticles(), save_articles_into_csv(), and save_articles_into_sql().

getArticles() sends a request to fetch the HTML content of the website, parses the HTML content using BeautifulSoup to find the  elements (headline, link, author, and date) of each article, and returns a pandas DataFrame with these articles.

save_articles_into_csv() takes a pandas DataFrame of articles as input and saves it to a CSV file.
