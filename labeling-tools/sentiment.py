from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from pathlib import Path
import pandas as pd
import json

class FinancialSentimentAnalyzer:
    def __init__(self):
        """
        Initialize the model using the 'ProsusAI/finbert' model, which is specifically
        trained on financial texts and is freely available on Hugging Face.
        """
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.labels = ["bearish", "neutral", "bullish"]

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of a given text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Contains sentiment label and confidence scores
        """
        # Tokenize the input text
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Get model outputs
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
        # Get the predicted sentiment and confidence scores
        sentiment_scores = predictions[0].numpy()
        predicted_label = self.labels[np.argmax(sentiment_scores)]

        return {
            "sentiment": predicted_label,
            "confidence_scores": {
                label: float(score) 
                for label, score in zip(self.labels, sentiment_scores)
            }
        }
    
def read_tweets_from_file(file_path):
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    tweets = []
    popularities = []
                
    if file_path.suffix.lower() == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for record in data:
                tweets.append(record['text'])

                fav = record['favorite_count']
                quote = record['quote_count']
                reply = record['reply_count']
                retweet = record['retweet_count']
                popularities.append(calculate_popularity_score(fav, quote, reply, retweet))
    
    return tweets, popularities

def analyze_tweets(tweets, popularity):
    analyzer = FinancialSentimentAnalyzer()
    results = []
    index = 0
    for tweet in tweets:
        sentiment_result = analyzer.analyze_sentiment(tweet)
        
        results.append({
            "tweet": tweets[index],
            "sentiment": sentiment_result["sentiment"],
            "confidence_scores": sentiment_result["confidence_scores"],
            "popularity": popularity[index]
        })
        index += 1
    
    return results

def calculate_popularity_score(favorite_count, quote_count, reply_count, retweet_count):
  favorite_weight = 0.1
  quote_weight = 0.3
  reply_weight = 0.2
  retweet_weight = 0.4

  score = (favorite_count * favorite_weight) + (quote_count * quote_weight) + (reply_count * reply_weight) + (retweet_count * retweet_weight)

  return score

def jsondump(results):
    with open('output_results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

if __name__ == "__main__":
    tweet_results, popularity_results = read_tweets_from_file("sentimentdata.json")
    analyze_tweet_results = analyze_tweets(tweet_results, popularity_results)

    for result in analyze_tweet_results:
        print(f"\nTweet: {result['tweet']}")
        print(f"Sentiment: {result['sentiment']}")
        print("Confidence Scores:")
        for sentiment, score in result['confidence_scores'].items():
            print(f"  {sentiment}: {score:.3f}")
        print(f"Popularity: {result['popularity']}")

    jsondump(analyze_tweet_results)

