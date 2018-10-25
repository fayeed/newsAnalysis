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

class Extractor:
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
