import keras
import numpy as np
from keras.preprocessing.text import Tokenizer
import pandas as pd
from keras.layers import Dense
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Input, Dense, Dropout, Embedding, LSTM, Conv1D
from keras.models import Model
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import simplejson
from sklearn.externals import joblib

# Text preprocessing steps
train_data = pd.read_csv('data/clean/emotion_classification.csv')
train_data['target'] = train_data.sentiment.astype('category').cat.codes
num_class = len(np.unique(train_data.sentiment.values))
y = train_data['target'].values

#  Tokenizing the words into flaots
MAX_LENGTH = 100
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_data.content.values)
post_seq = tokenizer.texts_to_sequences(train_data.content.values)
post_seq_padded = pad_sequences(post_seq, maxlen=MAX_LENGTH)

# slipting the dataset
X_train, X_test, y_train, y_test = train_test_split(
    post_seq_padded, y, test_size=0.05)

vocab_size = len(tokenizer.word_index) + 1

# creating the model 
inputs = Input(shape=(MAX_LENGTH, ))
embedding_layer = Embedding(vocab_size,
                            128,
                            input_length=MAX_LENGTH)(inputs)

x = Conv1D(128, 5, activation='relu')(embedding_layer)
x = LSTM(64, input_shape=(32, 32), return_sequences=True)(x)
x = Dropout(0.1)(x)
x = LSTM(32, input_shape=(32, 32))(x)
x = Dropout(0.1)(x)
x = Dense(10, activation='relu')(x)
x = Dropout(0.1)(x)

predictions = Dense(num_class, activation='softmax')(x)
model = Model(inputs=[inputs], outputs=predictions)
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['acc'])

model.summary()
filepath = "models/emotion_classifier_weights.hdf5"
checkpointer = ModelCheckpoint(
    filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
history = model.fit([X_train], batch_size=64, y=to_categorical(y_train), verbose=1, validation_split=0.1,
                    shuffle=True, epochs=10, callbacks=[checkpointer])

model_json = model.to_json()
with open("models/model.json", "w") as json_file:
    json_file.write(simplejson.dumps(simplejson.loads(model_json), indent=4))

with open('models/word_tokenizer.sav', 'wb') as f:
    joblib.dump(tokenizer, f)

# predicted valeu
predicted = model.predict(X_test)
predicted = np.argmax(predicted, axis=1)
print("Accuracy Score" + str(accuracy_score(y_test, predicted)))