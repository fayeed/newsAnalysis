import spacy
from flashtext import KeywordProcessor
import pickle
from spacy.lang.en.stop_words import STOP_WORDS
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from scipy.sparse import hstack
from sklearn.externals import joblib
from sklearn.preprocessing import normalize

article = [u"""The Bharatiya Janata Party (BJP) on Wednesday demanded from Delhi Chief Minister Arvind Kejriwal to remove Cabinet Minister Kailash Gahlot from his post. Earlier in the day, Income Tax sleuths carried out searches at 16 residential and business premises linked to Gahlot and his family members in the national capital and Gurugram.
"Kejriwal should immediately remove Gahlot as Transport Minister in view of the Income Tax raids at his 16 premises in connection with business operated and owned by his family," leader of Opposition in Delhi Assembly and BJP leader Vijender Gupta said in a statement here.
"Today, another gem of Kejriwal's 67 gems got exposed," he said adding that the Income Tax Department was not allowed to work in an independent and fair manner. 
Meanwhile, Kejriwal asked Prime Minister Narendra Modi to apologise for 'constantly troubling' the Aam Aadmi Party (AAP) government after the Income Tax Department carried out raids.
Kejriwal accused the Modi government of trying to 'intimidate' the AAP dispensation by getting its leaders and ministers raided by central agencies.
The party also termed the raid as 'political vendetta'.
"Friendship with Nirav Modi and Mallya and raid on us? Modiji you conducted raids on me Satyendar and Manish what happened to those (raids). Nothing was found. So before you go with another raid at least apologise to Delhi people for troubling their elected government," Kejriwal tweeted.""",
           u"""West Bengal chief minister and Trinamool Congress (TMC) chief Mamata Banerjee's efforts to rename the state as 'Bangla' have again faced an obstacle from the Ministry of Home Affairs (MHA).
According to The Indian Express, the home ministry has expressed concern over this move, saying that the name "may sound like Bangladesh and that it would be difficult to differentiate the two at international forums". The home ministry has written to the Ministry of External Affairs, the report said, to obtain an opinion before any further consideration.
However, in 2016, Mamata had addressed the possibility of the name being confused with Bangladesh. Noting that the name 'Bangla' had historical significance, she had said, "In English it will be Bengal, so that there will be no confusion with the name of neighbouring Bangladesh."
A constitutional amendment is required for a change in the name of a state. A recent example of the name of a state being changed was that of Odisha (earlier called Orissa).
Banerjee's plans to rename the state have been taking shape since 2011, when the newly elected chief minister had put forward 'Paschim Banga' as an option.
Banerjee's effort in 2011 never saw the light of day at the Centre, and was unsuccessful even in 2016 when the state Assembly passed a resolution to change the name of West Bengal to language-specific names. The cabinet had proposed that the name of the state be 'Bengal' in English, 'Bangla' in Bengali, and 'Bangal' in Hindi. Then, the home ministry had rejected the proposal saying that it would not be possible for a state to have different names in different languages.
However, in July this year, the West Bengal Assembly unanimously passed a resolution to change the state's name to 'Bangla'.
According to reports, the state's Assembly pushed more strongly for the renaming after the July 2016 Inter-State Council meeting in Delhi, when Banerjee was the last chief minister to address the Council because the speakers were listed in alphabetical order of the states. The name 'Bangla' would bump the state up in an alphabetically-organised list to number four.
Apart from political repercussions of the move to rename the state, with the Left, Congress, and BJP state parties walking out of the Assembly in August 2016 over the issue, political analysts have warned against reigniting tensions in the Darjeeling and Kalimpong areas of the state. People residing in "the hills" as the areas are colloquially referred to, had in 2017 initiated a strong resistance to the state government's move to make Bengali a mandatory language in schools in the state.
The Gorkha and Nepali communities of the state demanded a separate state "Gorkhaland" in protest and as an assertion of the linguistic differences in the state. Even though those protests were successfully pacified by the Mamata Banerjee-government after three months, experts believe that there continues to be a divide in socio-cultural aspects in the state.
As this report by Marcus Dam points out, the attempt to rename the state may not go down well in the hills, as "Bangla" is also the locally accepted term for the Bengali language."""]


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
        self.emotion_class, self.emotion_intensities, self.emotions_intensities_cat = self.getEmotion(
            article)

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
        return pos_counts

    def getEmotion(self, article):
        with open('models/model.json') as f:
            json = f.read()
            classification_model = model_from_json(json)

        classification_model.load_weights(
            'models/emotion_classifier_weights.hdf5')
        anger_model = joblib.load('models/intensity_anger.sav')
        fear_model = joblib.load('models/intensity_fear.sav')
        joy_model = joblib.load('models/intensity_joy.sav')
        sadness_model = joblib.load('models/intensity_sadness.sav')

        text = article.split('.')

        tokenizer = joblib.load('models/word_tokenizer.sav')
        vectorizer_anger = joblib.load('models/intensity_token_anger.sav')
        vectorizer_fear = joblib.load('models/intensity_token_fear.sav')
        vectorizer_joy = joblib.load('models/intensity_token_joy.sav')
        vectorizer_sadness = joblib.load('models/intensity_token_sadness.sav')

        post_seq = tokenizer.texts_to_sequences(text)
        post_seq_padded = pad_sequences(post_seq, maxlen=100)
        classification_pred = classification_model.predict(post_seq_padded)
        classification_pred = np.argmax(classification_pred, axis=1)

        intensity_list = []
        final_intensity_list = [0, 0, 0, 0]

        for index, p in enumerate(classification_pred.tolist()):
            if p == 0:
                vect_text = vectorizer_anger.transform([text[index]])
                vect_text = hstack([vect_text])
                intensity = anger_model.predict(vect_text)
                intensity_list.append(intensity)
                final_intensity_list[0] += intensity
            elif p == 1:
                vect_text = vectorizer_fear.transform([text[index]])
                vect_text = hstack([vect_text])
                intensity = fear_model.predict(vect_text)
                intensity_list.append(intensity)
                final_intensity_list[1] += intensity
            elif p == 2:
                vect_text = vectorizer_joy.transform([text[index]])
                vect_text = hstack([vect_text])
                intensity = joy_model.predict(vect_text)
                intensity_list.append(intensity)
                final_intensity_list[2] += intensity
            elif p == 3:
                vect_text = vectorizer_sadness.transform([text[index]])
                vect_text = hstack([vect_text])
                intensity = sadness_model.predict(vect_text)
                intensity_list.append(sadness_model.predict(vect_text))
                final_intensity_list[3] += intensity

        final_intensity_list = np.array(final_intensity_list).reshape(4,)
        final_intensity_list = normalize(
            final_intensity_list[:, np.newaxis], axis=0).ravel()
        return classification_pred, intensity_list, final_intensity_list


if __name__ == "__main__":
  for index, a in enumerate(article):
      news = NewsDataExtractor(a)
      print('------------------------------------------ {} -----------------------------------------'.format(index))
      print("Cities : {} \n\nPoliticains : {} \n\nStates : {}\n".format(news.cities, news.politicains, news.states))
      print("Persons : {} \n\nOrganiztion : {}\n".format(news.persons, news.organization))
      print("Commons Words : {}\n".format(news.commonWords))
      print("Emotions Classification : {}\n\nEmotion Intensities : {}\n\nEmotion Intensities Category : {}".format(news.emotion_class, news.emotion_intensities,
            news.emotions_intensities_cat))
      print('----------------------------------------------------------------------------------------\n\n')
