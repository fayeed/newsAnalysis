from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

finalList = []

url = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"

page = urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

items = soup.select('.wikitable > tbody > tr > th > a')

list = [item.text.replace("-", " ") for item in items]

with open('scrapper_data/states', 'wb') as fb:
  pickle.dump(list, fb)