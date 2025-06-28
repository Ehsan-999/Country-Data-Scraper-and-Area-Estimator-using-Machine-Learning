from bs4 import BeautifulSoup
import requests
import re
import pymysql
from sklearn import tree
import numpy as np
from sklearn.tree import DecisionTreeRegressor

url = "https://scrapethissite.com/pages/simple/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

countries = soup.select(".country")

data = []
x = []
y=[]
for country in countries:
    name = country.find("h3", class_="country-name").text.strip()
    capital = country.find("span", class_="country-capital").text.strip()
    population = country.find("span", class_="country-population").text.strip().replace(",", "")
    area = country.find("span", class_="country-area").text.strip().replace(",", "")
    x.append(int(population))
    y.append(float(area))
    data.append((name, capital, int(population), float(area)))

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="qazwsx129",  
    database="testdb",       
    charset="utf8mb4"
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        capital VARCHAR(100),
        population INT,
        area FLOAT
    )
""")

for row in data:
    cursor.execute("INSERT INTO countries (name, capital, population, area) VALUES (%s, %s, %s, %s)", row)



x = np.array(x).reshape(-1, 1)
y = np.array(y)

model = DecisionTreeRegressor()
model.fit(x, y)


new_data = np.array([120000]).reshape(-1, 1)
answer = model.predict(new_data)

print(answer[0])
conn.commit()
cursor.close()
conn.close()

