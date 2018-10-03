from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

finalList = []
politicainList = []

url = "https://en.wikipedia.org/wiki/Category:Indian_politicians_by_city_or_town"

page = urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

items = soup.select('.CategoryTreeLabel')

citiesList = [ "https://en.wikipedia.org" + item['href'] for item in items]

for city in citiesList:
  print(city)
  page = urlopen(city)
  soup = BeautifulSoup(page, 'html.parser')
  items = soup.select('.mw-category-group > ul > li > a')
  list = [item.text for item in items]
  finalList = finalList + list


with open('../scrapper_data/politicains.txt', 'wb') as fb:
  pickle.dump(finalList, fb)
