import json

INPUT_FILE_PATH = 'labeled-data/data.json'
OUTPUT_FILE_PATH = 'labeled-data/data.json'

def get_popularity(favorite_count, reply_count, retweet_count):
    return favorite_count + 2 * reply_count + 3 * retweet_count

with open(INPUT_FILE_PATH, "r") as json_file:
    data = json.load(json_file)

    labeled_data = []

    with open(OUTPUT_FILE_PATH, "w") as file:
        json.dump(labeled_data, file)