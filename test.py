import spacy
from flashtext import KeywordProcessor
import pickle

CITIES = './scrapper_data/cities.txt'
POLITICAINS = './scrapper_data/politicains.txt'
STATES = './scrapper_data/states.txt'

article = u"""Noida: Uttar Pradesh governor Ram Naik on Thursday said the name of the father of the Constitution BR Ambedkar should be corrected in the entire country and it was not right to politicise the issue.

File image of Uttar Pradesh governor Ram Naik. News18File image of Uttar Pradesh governor Ram Naik. News18
His remarks came a day after the state government issued an order on using 'Ramji' as Ambedkar's middle name in all references to him in official correspondence and records. Following the decision, the Opposition parties had alleged that the government was doing vote bank politics ahead of the 2019 Lok Sabha elections.

'Ramji' was the name of Ambedkar's father and as per practice in Maharashtra, father's name is used as the middle name by his son, Naik said.

The spelling of Ambedkar in English will remain unchanged, but in Hindi it will be spelt as 'Aambedkar'.

Ambedkar's statues should be put with his correct name in all official departments in the state, Naik said, while speaking at an event in Indira Gandhi Kala Kendra in Noida.


The governor said the name should be corrected in the entire country and a letter had already been written to President Ram Nath Kovind and Home Minister Rajnath Singh in this regard.


Naik, in December 2017, had started a campaign to write Ambedkar's name in the correct way."""

def tag(file, news):
  with open(file, 'rb') as fb:
    keywords = pickle.load(fb)
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_list(keywords)

  keywords_found = keyword_processor.extract_keywords(news)
  sets = set()
  for k in keywords_found:
    sets.add(k)

  return sets

nlp = spacy.load('en')
doc = nlp(article)

for entity in doc:
  print(entity)

print(tag(CITIES, article), tag(POLITICAINS, article))