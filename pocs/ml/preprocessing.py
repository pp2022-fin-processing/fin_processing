import string
import nltk
from nltk.stem import WordNetLemmatizer
import os
import pandas as pd


class Nlp:
    def __init__(self, text: str):
        self.text = text

    def remove_punctuation(self):
        return "".join([i for i in self.text if i not in string.punctuation])

    def to_lower_case(self):
        return self.text.lower()

    def split_to_words(self):
        return self.text.split(" ")

    def remove_stopwords(self):
        # nltk.download('stopwords')
        stopwords = nltk.corpus.stopwords.words('english')
        return [i for i in self.text if i not in stopwords]

    def lemmatize(self):
        # nltk.download('popular')
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in self.text]

    def apply(self, f):
        output = f(self.text)
        print(output)
        self.text = output


def read_sentiment_file():
    sentiments = dict()
    sentiment_file = open(os.path.join("..", "..", "data", "word_sentiment", "sentiment_dictionary.csv"))
    sentiment_file.readline()
    for line in sentiment_file:
        word = line.split(",")[0].lower()
        sentiment = line.split(",")[1].replace("\n", "")
        sentiments[word] = sentiment
    return sentiments


article = open("big_tech_again")
data = article.read().replace("\n", " ")
print(data)

nlp = Nlp(data)
nlp.apply(lambda x: nlp.remove_punctuation())
nlp.apply(lambda x: nlp.to_lower_case())
nlp.apply(lambda x: nlp.split_to_words())
nlp.apply(lambda x: nlp.remove_stopwords())
nlp.apply(lambda x: nlp.lemmatize())

sentiment = read_sentiment_file()
sentiment_counter = {"N": [0], "P": [0], "U": [0]}
for word in nlp.text:
    if word in sentiment:
        if sentiment[word] == "N":
            sentiment_counter["N"][0] += 1
        elif sentiment[word] == "P":
            sentiment_counter["P"][0] += 1
        elif sentiment[word] == "U":
            sentiment_counter["U"][0] += 1
print(sentiment_counter["P"][0], " ", sentiment_counter["N"][0], " ", sentiment_counter["U"][0])

df = pd.DataFrame(sentiment_counter)
print(df)
