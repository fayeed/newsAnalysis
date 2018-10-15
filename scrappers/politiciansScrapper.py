from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import re
import pickle

ssl._create_default_https_context = ssl._create_unverified_context

finalList = set()
politicainList = []

def getNames(url, callback):
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  page = urlopen(req)
  soup = BeautifulSoup(page, 'html.parser')
  callback(soup)

def getWikiCities(soup):
  items = soup.select('.CategoryTreeLabel')
  citiesList = ["https://en.wikipedia.org" + item['href'] for item in items]
  for city in citiesList:
    print(city)
    page = urlopen(city)
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.select('.mw-category-group > ul > li > a')
    list = [item.text for item in items]
    for l in list:
      finalList.add(l)

def getRajyaSabha(soup):
  items = soup.select('.tabletimeline > tbody > tr > td')
  items = items[3:]
  for i in range(1, len(items)-1, 3):
    finalList.add(items[i].text)

def getLockSabha(soup):
  items = soup.select('#Tab1 > tbody > tr > td')
  items = items[3:]
  for i in range(0, len(items)-1, 3):
    names = items[i].text.split(",")
    finalList.add(names[1][1:])

def getCM(soup):
  items = soup.select('.tabletimeline > tbody > tr > td')
  items = items[4:]
  for i in range(2, len(items)-1, 4):
    finalList.add(items[i].text)

def getCongressSabha(soup):
  items = soup.select('.secretaries-content > h3')
  for i in items:
    finalList.add(i.text)

def getCongressPresident(soup):
  items = soup.select('.secretaries-content > h3')
  for i in range(0, len(items)-1, 2):
    finalList.add(items[i].text)

def getCMLeaders(soup):
  items = soup.select('.rtejustify > p')
  items = items[3:]
  for i in range(0, len(items)-1, 2):
    n = items[i].text.split("\n")
    for c in n:
      c = re.split("[0-9].", c)
      if len(c) > 1:
        c = c[1]
      else:
        c = c[0]

if __name__ == "__main__":
  getNames("https://en.wikipedia.org/wiki/Category:Indian_politicians_by_city_or_town", getWikiCities)
  getNames("http://www.bjp.org/bjp-in-parliament/rajya-sabha-members", getRajyaSabha)
  getNames("http://www.bjp.org/bjp-in-parliament/lok-sabha-members", getLockSabha)
  getNames("http://www.bjp.org/leadership/chief-ministers", getCM)
  getNames("https://www.inc.in/en/lok-sabha-members?page=1", getCongressSabha)
  getNames("https://www.inc.in/en/lok-sabha-members?page=2", getCongressSabha)
  getNames("https://www.inc.in/en/lok-sabha-members?page=3", getCongressSabha)
  getNames("https://www.inc.in/en/rajya-sabha-members?page=1", getCongressSabha)
  getNames("https://www.inc.in/en/rajya-sabha-members?page=2", getCongressSabha)
  getNames("https://www.inc.in/en/rajya-sabha-members?page=3", getCongressSabha)
  getNames("https://www.inc.in/en/pcc-presidents?page=1", getCongressPresident)
  getNames("https://www.inc.in/en/pcc-presidents?page=2", getCongressPresident)
  getNames("https://www.inc.in/en/pcc-presidents?page=3", getCongressPresident)
  getNames("https://www.inc.in/en/pcc-presidents?page=4", getCongressPresident)
  getNames("https://www.inc.in/en/clp-leaders?page=1", getCongressPresident)
  getNames("https://www.cpim.org/leadership", getCMLeaders)
  with open('scrapper_data/politicains', 'wb') as fb:
    pickle.dump(list(finalList), fb)