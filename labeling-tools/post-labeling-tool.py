import json

INPUT_FILE_PATH = 'data/raw-data/data2.json'
OUTPUT_FILE_PATH = 'data/labeled-data/data2.json'

def get_popularity(favorite_count, reply_count, retweet_count):
    return favorite_count + 2 * reply_count + 3 * retweet_count

with open(INPUT_FILE_PATH, "r") as json_file:
    data = json.load(json_file)

    labeled_data = []

    if isinstance(data, list):
        for post in data:
            text = post.get('text', 'ERROR')
            print(text)
            sentiment = input('Type 1 for bullish, 2 for bearish, 3 for neutral, 4 for ignore, 5 to exit:')
            if sentiment == '1':
                sentiment = 'bullish'
            elif sentiment == '2':
                sentiment = 'bearish'
            elif sentiment == '3':
                sentiment = 'neutral'
            elif sentiment == '4':
                continue
            elif sentiment == '5':
                break
            tickers = input('Tickers split by ",":').split(',')
            popularity = get_popularity(int(post.get('favorite_count', 0)), int(post.get('reply_count', 0)),
                                        int(post.get('retweet_count', 0)))

            labeled_data.append(
                {
                    'text': text,
                    'tickers': tickers,
                    'sentiment': sentiment,
                    'popularity': popularity
                }
            )

    with open(OUTPUT_FILE_PATH, "w") as file:
        json.dump(labeled_data, file)