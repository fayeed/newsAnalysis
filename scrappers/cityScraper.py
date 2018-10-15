from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

finalList = []

url = "http://www.parentingnation.in/India"

page = urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

items = soup.select('.product-review > ul > li > a')

list = [item.text.replace("-", " ") for item in items]

for l in list:
  temp = l.split(" ")
  if len(temp) == 1:
    tempList = [l]
  else:
    tempList = [l] + temp

  finalList.append(tempList)

with open('scrapper_data/cities', 'wb') as fb:
  pickle.dump(list, fb)