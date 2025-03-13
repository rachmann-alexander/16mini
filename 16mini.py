# pip install requests beautifulsoup4


import sqlite3
import requests
from bs4 import BeautifulSoup


conn = sqlite3.connect("web_data.db")
cursor = conn.cursor()


cursor.execute('DROP TABLE IF EXISTS articles')
cursor.execute('''
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT
)
''')


url = "https://www.heise.de/"  
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)


soup = BeautifulSoup(response.text, "html.parser")


articles = soup.find_all("article")  

cursor.execute("DELETE FROM articles") 


for article in articles:
    title = article.find("h3").text.strip()
    link = "https://www.heise.de" + article.find("a")["href"]  
    cursor.execute("INSERT INTO articles (title, link) VALUES (?, ?)", (title, link))


conn.commit()


cursor.execute("SELECT title, link FROM articles WHERE title LIKE '% KI %' ORDER BY title DESC LIMIT 10")
ki_articles = cursor.fetchall()
for article in ki_articles:
    print(article)

conn.close()
