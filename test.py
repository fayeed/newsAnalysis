from emotion import Extractor
import json


def aggregate(arr):
    final = {
        'anger': 0,
        'fear': 0,
        'joy': 0,
        'sadness': 0
    }
    for i, a in enumerate(arr):
        if a == 0:
            final['anger'] = final['anger'] + 1
        elif a == 1:
            final['fear'] = final['fear'] + 1
        elif a == 2:
            final['joy'] = final['joy'] + 1
        elif a == 3:
            final['sadness'] = final['sadness'] + 1

    return final


if __name__ == "__main__":
    with open('articles.json', 'r') as f:
        articles = json.load(f)
        for index, a in enumerate(articles):
            news = Extractor(a['body'])
            cat = aggregate(news.emotion_class)
            norm = [float(i)/sum(news.emotions_intensities_cat)
                    for i in news.emotions_intensities_cat]
            print('------------------------------------------ {} -----------------------------------------'.format(index))
            print("Cities : {} \n\nPoliticains : {} \n\nStates : {}\n".format(
                news.cities, news.politicains, news.states))
            print("Persons : {} \n\nOrganiztion : {}\n".format(
                news.persons, news.organization))
            print("Commons Words : {}\n".format(news.commonWords))
            print("Emotions Classification : {}\n\nEmotion Intensities Category : {}".format(cat,
                                                                                             norm))
            print(
                '----------------------------------------------------------------------------------------\n\n')
