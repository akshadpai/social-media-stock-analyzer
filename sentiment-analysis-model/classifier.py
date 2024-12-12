import json
from model import NaiveBayesClassifier

TRAINING_DATA_FILE_PATH = 'data/labeled-data/data2.json'
INPUT_FILE_PATH = 'data/raw-data/data3.json'
TICKER_FILE_PATH = 'sentiment-analysis-model/tickers.json'
OUTPUT_FILE_PATH = 'data/labeled-data/classified/data3.json'

def get_popularity(favorite_count, reply_count, retweet_count):
    return favorite_count + 2 * reply_count + 3 * retweet_count

def get_tickers(text, ticker_map):
    text = text.lower()
    ticker_list = []
    for ticker in ticker_map:
        if ticker.lower() in text:
            ticker_list.append(ticker_map[ticker].upper())
    return ticker_list

with open(TRAINING_DATA_FILE_PATH, "r") as json_file:
    training_data = json.load(json_file)

    model = NaiveBayesClassifier(categories=['bullish', 'bearish', 'neutral'], category_smoothing=1, word_smoothing=1)
    documents = [post['text'] for post in training_data]
    labels = [post['sentiment'] for post in training_data]
    model.train(documents, labels)

    raw_data = []
    with open(INPUT_FILE_PATH, 'r') as input_file:
        raw_data = json.load(input_file)

    classified_data = []
    tickers = {}
    with open(TICKER_FILE_PATH, "r") as tickers_file:
        tickers = json.load(tickers_file)
    for post in raw_data:
        document = post['text']
        popularity = get_popularity(int(post['favorite_count']), int(post['reply_count']), int(post['retweet_count']))
        classified_data.append(
            {
                'text': document,
                'sentiment': model.classify(document),
                'tickers': get_tickers(document, tickers),
                'popularity': popularity
            }
        )

    with open(OUTPUT_FILE_PATH, "w") as file:
        json.dump(classified_data, file)