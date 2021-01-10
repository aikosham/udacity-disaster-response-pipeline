import sys
import pandas as pd
from sqlalchemy import create_engine
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download(['punkt', 'wordnet'])
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle


def load_data(database_filepath):
    """
    Load data from database.
    Input: filepath to database
    """
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table(database_filepath,engine)
    X = df.loc[:,'message']
    Y = df.iloc[:,-36:]
    category_names=list(Y.columns)
    return X,Y,category_names


def tokenize(text):
    """
    Tokenize & process text data.
    Input: text data to be cleaned and tokenized
    """
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    """Returns model with machine learning pipeline."""
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer(use_idf=True)),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
         ])

# Note: commented out because it takes too long to train the model. Have passed in output of cv.best_params_ into pipeline above.
    parameters = {
        'vect__ngram_range': ((1, 1), (1, 2)),
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__max_features': (None, 5000, 10000),
        'tfidf__use_idf': (True, False),
        'clf__estimator__n_estimators': [50, 100, 200],
        'clf__estimator__min_samples_split': [2, 3, 4],
    }

    cv = GridSearchCV(pipeline, param_grid=parameters, n_jobs=-1)

    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    """
    Returns classification report for each category classified by the model.
    Inputs:
    - model: trained model
    - X_test: features in test dataset  to be used by model
    - Y_test: categories/output  in test dataset to be evaluated against predicted output by model
    - category_names: names of all output categories that can be classified
    """
    y_pred = model.predict(X_test)
    for a,b in enumerate(category_names):
        print("For column {}:".format(b))
        print(classification_report(Y_test[b], y_pred[:,a]))
    # print("\nsBest Parameters:", cv.best_params_)


def save_model(model, model_filepath):
    """
    Exports model as a pickle file.
    Inputs:
    - model: final trained model
    - model_filepath: filepath destination to where model will be exported as pickle file
    """
    filename = model_filepath
    pickle.dump(model, open(filename, 'wb'))

def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
