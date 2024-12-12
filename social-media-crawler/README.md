## X (formerly Twitter) Social Media Crawler
We have a Twitter Scraper in place to scrape posts by keywords or tickers.
This scraper can get tweet text, engagement counts, and comments associated with the tweet.
Initially, we were trying to look for official API to do this but it comes with pricing so we went with HTTP request instead. 
In order to do that, we got the request API by inspecting the network call in browser and then replicate that request in Python. Plus, we need cookie as an authentication to the twitter account.  
We can then specify the tickers for companies as keywords and input that into our scraper. It will then scrape the tweet related to those tickers or keywords.


---

### How to initialize the scraper
```bash
scraper = TwitterScraper(
      cookie='TWITTER_COOKIE_HERE',
      csrf_token='TWITTER_CSRF_TOKEN_HERE',
   )
```
In order to get cookie and CSRF token, log in to your Twitter/X account and then get cookie and csrf_token from Network tab in Chrome developer tools.

---

### How to start the tweets search
```bash
scraper.search(term='KEYWORD HERE', limit=40, search_type=SearchType.LATEST)
```

---
### How to get comments associate with the tweet
```bash
scraper.get_comments(TWEET_ID)
```

---

### Limitation
Make sure to also aware of rate limit. When it happens, we need to switch to new Twitter account.

---