import json

INPUT_FILE_PATH = 'labeled_data.json'

class DataManager:
    def __init__(self):
        """
        Initialize the DataManager by loading JSON data from the file.
        """
        with open(INPUT_FILE_PATH, "r") as json_file:
            self.data = json.load(json_file)

    def get_data(self, ticker=None, sentiment=None, sort_by_popularity=None):
        """
        Retrieve filtered and sorted data. All parameters are optional

        :param ticker: A string representing the ticker to filter by (e.g., "AAPL").
        :param sentiment: A string representing the sentiment to filter by ("bullish", "bearish", "neutral").
        :param sort_by_popularity: A string "ASC" for ascending or "DESC" for descending sort order.
        :return: A list of filtered and sorted posts.
        """
        # Start with all data
        filtered_data = self.data

        # Filter by ticker
        if ticker:
            filtered_data = [
                post for post in filtered_data if ticker.upper() in post.get("tickers", [])
            ]

        # Filter by sentiment
        if sentiment:
            filtered_data = [
                post for post in filtered_data if post.get("sentiment") == sentiment
            ]

        # Sort by popularity
        if sort_by_popularity:
            reverse = sort_by_popularity.lower() == "desc"  # Sort descending if "desc"
            filtered_data = sorted(
                filtered_data, key=lambda x: x.get("popularity", 0), reverse=reverse
            )

        return filtered_data