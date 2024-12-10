from flask import Flask, render_template, request
from data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize default values or empty results
    ticker = ''
    sentiment_filter = ''
    sort_option = ''
    results = []

    if request.method == 'POST':
        ticker = request.form.get('ticker', '')
        sentiment_filter = request.form.get('sentiment', '')
        sort_option = request.form.get('sort', '')

        # Placeholder: This is where you would integrate your logic to:
        # 1. Retrieve posts related to the ticker (query)
        # 2. Filter by the sentiment (if bullish or bearish chosen)
        # 3. Sort by popularity (if chosen)
        #
        # For now, we just return an empty results list or some dummy data
        results = data_manager.get_data(ticker=ticker, sentiment=sentiment_filter, sort_by_popularity=sort_option)

    return render_template('index.html', results=results, query=ticker, sentiment_filter=sentiment_filter, sort_option=sort_option)



if __name__ == '__main__':
    app.run(debug=True)

