import spacy
from flashtext import KeywordProcessor
import pickle
from spacy.lang.en.stop_words import STOP_WORDS

article = u"""The Bharatiya Janata Party (BJP) on Wednesday demanded from Delhi Chief Minister Arvind Kejriwal to remove Cabinet Minister Kailash Gahlot from his post. Earlier in the day, Income Tax sleuths carried out searches at 16 residential and business premises linked to Gahlot and his family members in the national capital and Gurugram.
"Kejriwal should immediately remove Gahlot as Transport Minister in view of the Income Tax raids at his 16 premises in connection with business operated and owned by his family," leader of Opposition in Delhi Assembly and BJP leader Vijender Gupta said in a statement here.
"Today, another gem of Kejriwal's 67 gems got exposed," he said adding that the Income Tax Department was not allowed to work in an independent and fair manner. 
Meanwhile, Kejriwal asked Prime Minister Narendra Modi to apologise for 'constantly troubling' the Aam Aadmi Party (AAP) government after the Income Tax Department carried out raids.
Kejriwal accused the Modi government of trying to 'intimidate' the AAP dispensation by getting its leaders and ministers raided by central agencies.
The party also termed the raid as 'political vendetta'.
"Friendship with Nirav Modi and Mallya and raid on us? Modiji you conducted raids on me Satyendar and Manish what happened to those (raids). Nothing was found. So before you go with another raid at least apologise to Delhi people for troubling their elected government," Kejriwal tweeted."""

class NewsDataExtractor:
  def __init__(self, article):
    self.CITIES = 'scrapper_data/cities'
    self.POLITICAINS = 'scrapper_data/politicains'
    self.STATES = 'scrapper_data/states'
    nlp = spacy.load('en')
    self.doc = nlp(article)
    self.cities = self.tag(self.CITIES, article)
    self.politicains = self.tag(self.POLITICAINS, article)
    self.states = self.tag(self.STATES, article)
    self.nouns = self.getNoun()
    self.nounChunks = self.getNounChunk()
    self.adjective = self.getAdjective()
    self.organization = self.getOrganization()
    self.persons = self.getPersons()
    self.commonWords = self.getCommonWords()

  def tag(self, file, news):
    with open(file, 'rb') as fb:
      keywords = pickle.load(fb)
      keyword_processor = KeywordProcessor()
      keyword_processor.add_keywords_from_list(keywords)

    keywords_found = keyword_processor.extract_keywords(news)
    sets = set()
    for k in keywords_found:
      sets.add(k)

    return sets

  def getNoun(self):
    finalList = set()
    for np in self.doc.noun_chunks:
      finalList.add(np.root.text)
    return list(finalList)

  def getNounChunk(self):
    finalList = set()
    for np in self.doc.noun_chunks:
      finalList.add(np.text)
    return list(finalList)

  def getAdjective(self):
    finalList = set()
    for token in self.doc:
      if token.pos_ == "ADJ":
        finalList.add(token)
    return list(finalList)

  def removeDuplicates(self, list):
    for city in self.cities:
      if city in list:
        list.remove(city)
    for state in self.states:
      if state in list:
        list.remove(state)
    return list

  def getOrganization(self):
    finalList = set()
    for entity in self.doc.ents:
      if entity.label_ == "ORG":
        finalList.add(entity.text)
    finalList = self.removeDuplicates(finalList)
    return list(finalList)

  def getPersons(self):
    finalList = set()
    for entity in self.doc.ents:
      if entity.label_ == "PERSON":
        finalList.add(entity.text)
    finalList = self.removeDuplicates(finalList)
    return list(finalList)

  def getCommonWords(self):
    pos_counts = {}
    for np in self.doc.noun_chunks:
      if pos_counts.get(np.root.text.lower()) == None:
        pos_counts[np.root.text.lower()] = 1
      else:
        pos_counts[np.root.text.lower()] += 1
    print(pos_counts)










news = NewsDataExtractor(article)

# print(news.getPersons(), news.getOrganization())
# print(news.cities, news.politicains, news.states)
print(news.getCommonWords())