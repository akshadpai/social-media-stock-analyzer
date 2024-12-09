from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize default values or empty results
    query = ''
    sentiment_filter = ''
    sort_option = ''
    results = []

    if request.method == 'POST':
        query = request.form.get('query', '')
        sentiment_filter = request.form.get('sentiment', '')
        sort_option = request.form.get('sort', '')

        # Placeholder: This is where you would integrate your logic to:
        # 1. Retrieve posts related to the ticker (query)
        # 2. Filter by the sentiment (if bullish or bearish chosen)
        # 3. Sort by popularity (if chosen)
        #
        # For now, we just return an empty results list or some dummy data
        results = [
            {
                'ticker': 'AAPL',
                'company_name': 'Apple Inc.',
                'text': 'I think AAPL is going to soar this quarter!',
                'sentiment': 'Bullish',
                'popularity': 123
            },
            {
                'ticker': 'TSLA',
                'company_name': 'Tesla, Inc.',
                'text': 'I am not confident in TSLA’s future right now.',
                'sentiment': 'Bearish',
                'popularity': 98
            }
        ]

        # Filtering logic (dummy)
        if query:
            results = [r for r in results if query.upper() in r['ticker']]

        if sentiment_filter == 'bullish':
            results = [r for r in results if r['sentiment'].lower() == 'bullish']
        elif sentiment_filter == 'bearish':
            results = [r for r in results if r['sentiment'].lower() == 'bearish']

        if sort_option == 'popularity':
            results = sorted(results, key=lambda x: x['popularity'], reverse=True)

    return render_template('index.html', results=results, query=query, sentiment_filter=sentiment_filter, sort_option=sort_option)



if __name__ == '__main__':
    app.run(debug=True)
