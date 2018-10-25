import pandas
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Ridge
from scipy.sparse import hstack
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


def get_data(filename):
    df = pandas.read_csv(filename)
    df['content'] = df['content'].str.lower().replace(
        '[^a-zA-Z0-9]', ' ', regex=True)
    return df


train_fn = ['data/clean/emotion_anger_regression.csv', 'data/clean/emotion_fear_regression.csv', 'data/clean/emotion_joy_regression.csv', 'data/clean/emotion_sadness_regression.csv']

classes = ['anger', 'fear', 'joy', 'sadness']

for index, t in enumerate(train_fn):
  train = get_data(t)

  vectorizer = TfidfVectorizer(min_df=5)
  enc = DictVectorizer()
  model = Ridge(alpha=1.0, random_state=241,)

  X_train = vectorizer.fit_transform(train['content'])
  X_train = hstack([X_train])

  X_train, X_test, y_train, y_test = train_test_split(
      X_train, train['sentiment_value'], test_size=0.05)

  # train the model
  model.fit(X_train, y_train)
  rslt = model.predict(X_test)
  print(model)
  score = np.sqrt(mean_squared_error(rslt, y_test))
  
  model_filename = 'models/intensity_{}.sav'.format(classes[index])
  joblib.dump(model, model_filename)

  token_filename = 'models/intensity_token_{}.sav'.format(classes[index])
  joblib.dump(vectorizer, token_filename)



if __name__ == "__main__":
    loaded_model = joblib.load(model_filename)
    result = model.predict(X_test)
    score = np.sqrt(mean_squared_error(rslt, y_test))
    print(score)
