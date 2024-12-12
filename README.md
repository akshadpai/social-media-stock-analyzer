```markdown
# Social Media Stock Analyzer

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Modules and Features](#modules-and-features)
6. [Data Description](#data-description)

---

## Introduction
The **Social Media Stock Analyzer** project uses sentiment analysis to evaluate the impact of social media activity on stock prices. The tool provides data crawling, labeling, and analysis capabilities through an intuitive web application.

---

## Project Structure

```
social-media-stock-analyzer/
├── data/
│   ├── classified/          # Processed and classified datasets
│   ├── labeled-data/        # Labeled datasets for training
│   ├── raw-data/            # Raw, unprocessed data
├── labeling-tools/
│   ├── post-labeling-tool.py    # Tool for manual data labeling
│   ├── sentiment.py             # Tool for automatic data labeling
├── sentiment-analysis-model/    # Code and resources for training the sentiment analysis model
│   ├── classifier.py/           # HTML templates for the web app
│   ├── model.py/                # Naive Bayes Classifier
│   ├── tickers.json/            # Defined tickers to scrape from data
├── social-media-crawler/
│   ├── twitter_scraper.py       # Script to scrape data from Twitter
├── web-application/
│   ├── templates/               # HTML templates for the web app
│   ├── data_manager.py          # Backend logic for managing data
│   ├── web_app.py               # Main web application script
├── README.md                    # Project documentation
```

---

## Installation
Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/akshadpai/social-media-stock-analyzer.git
   cd social-media-stock-analyzer

2. Define input and output files in the top of each file to specify data
   ```

---

## Usage
### Starting the Web Application
Run the web application:
```bash
python web-application/web_app.py
```
The app will be available at `http://localhost:5000`.

### Running the Social Media Crawler
To scrape data from Twitter:
```bash
python social-media-crawler/twitter_scraper.py
```

### Labeling Data
To label data using the provided tools:
```bash
python labeling-tools/post-labeling-tool.py
python labeling-tools/sentiment.py
```

---

## Modules and Features
### 1. **Data**
   - Stores raw, labeled, and classified datasets.

### 2. **Labeling Tools**
   - `post-labeling-tool.py`: A command-line tool for manual data labeling.
   - `sentiment.py`: Automates sentiment analysis labeling tasks.

### 3. **Sentiment Analysis Model**
   - Includes training scripts and resources for building the sentiment analysis model.
   - Implements a generative probabilistic model Naive Bayes using words, bigrams, and trigrams

### 4. **Social Media Crawler**
   - `twitter_scraper.py`: Fetches X social media posts for analysis.

### 5. **Web Application**
   - Provides an interface to view and manage the data and results.

---

## Data Description
- **Raw Data**: Unprocessed social media posts fetched by the crawler.
- **Labeled Data**: Data labeled with sentiment from manual or automated generation.
- **Classified Data**: Classified data generated by model ready for the user.