# Disaster Response Pipeline Project

## Motivation
In this project we apply data engineering, NLP, and ML to analyze message data that people sent during disasters to build model for an application that quickly classifies disaster messages. These messages can accelerate disaster response.

## Pre-requisites
The environment used is described in `requirements.txt` (Python 3.8.2 with packages in the requirements.txt file). Here is a brief overview of the packages that were used:
```
# NLP
punkt
wordnet
stopwords

# Visualization
plotly

# ML and data
pandas, scikitlearn, matplotlib
```

For the full environment details (including linters etc.) see `requirements.txt`

### File Description
```
.
├── app -------------------------------------> Code for Webapp
│   ├── run.py
│   └── templates
│       ├── go.html
│       └── master.html
├── data ------------------------------------> Messages data storage
│   ├── disaster_categories.csv
│   ├── disaster_messages.csv
│   └── process_data.py
├── models -----------------------------------> Training code
│   └── train_classifier.py
├── README.md
└── requirements.txt -------------------------> env setup
```

### Instructions:
The virtualenv I used is described in `requirements.txt`. So, `pip install -r requirements.txt` should set up the env.

1. Run the following commands in the project's root directory to set up database and model.
    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

## Results
- ETL pipeline to read data from CSV files, clean data and save to SQL database
- ML Pipeline to train classifier for all the categories in the dataset
- Flask app for visualization


