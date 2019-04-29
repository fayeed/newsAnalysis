# News Analysis

### Step 1: Install all the dependencies

`pip install -r requirements.txt`<br>
`python -m spacy download en`

### Step 2: Generate models

`python emotion_classification_data_builder.py`<br>
`python emotion_classifier.py`<br>
`python emotion_regressor_data_builder.py`<br>
`python emotion_intensity_builder.py`

### Step 3: Save articles

Save all the articles in a json file in array fromat with main articles content in a body property.<br>
See the `articles.json` file for a example.<br>
`Note: articles must JSON String escaped.`

### Step 3: Run the program

`python test.py`
