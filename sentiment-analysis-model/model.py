from collections import defaultdict
from collections import Counter
from math import log

def extract_ngrams(text):
    """
    Separates the input text into words, bigrams, and trigrams.

    :param text: The input string of text.
    :return: A tuple containing three lists: words, bigrams, and trigrams.
    """
    # Tokenize the text into words
    words = text.split()

    # Generate bigrams and trigrams
    bigrams = [words[i] + ' ' +  words[i + 1] for i in range(len(words) - 1)]
    trigrams = [words[i] + ' ' + words[i + 1] + ' ' + words[i + 2] for i in range(len(words) - 2)]

    return words, bigrams, trigrams

class NaiveBayesClassifier:
    def __init__(self, categories, category_smoothing, word_smoothing):
        self.categories = categories
        self.delta = category_smoothing
        self.mu = word_smoothing
        self.word_distributions = None
        self.vocabulary = None
        self.category_weights = None

    def classify(self, document):
        words, bigrams, trigrams = extract_ngrams(document)
        category_scores = []
        for category in self.categories:
            category_scores.append(self.calculate_category_score(category, words + bigrams + trigrams))

        category_idx = category_scores.index(max(category_scores))
        return self.categories[category_idx]


    def calculate_category_score(self, category, ngrams):
        score = log(self.category_weights[category])
        ngram_counts = dict(Counter(ngrams))
        for ngram in ngram_counts:
            score += ngram_counts[ngram] * log(self.word_distributions[category][ngram])
        return score

    def train(self, document_list, label_list):
        """
        Trains model based on labeled data

        :param document_list: List of documents
        :param label_list: List of labels to categorize documents. Must be same length as document_list
        :return: A tuple containing three lists: words, bigrams, and trigrams.
        """
        category_counts = {category : 0 for category in self.categories}
        ngram_counts = {category : defaultdict(int) for category in self.categories}
        ngram_total_count = 0
        vocabulary = set()

        print('Training Naive Bayes Classifier...')

        for i in range(len(document_list)):
            document = document_list[i]
            category = label_list[i]

            category_counts[category] += 1

            words, bigrams, trigrams = extract_ngrams(document)

            # Increment counts
            ngram_total_count += len(words) + len(bigrams) + len(trigrams)
            for word in words:
                vocabulary.add(word)
                ngram_counts[category][word] += 1
            for bigram in bigrams:
                vocabulary.add(bigram)
                ngram_counts[category][bigram] += 1
            for trigram in trigrams:
                vocabulary.add(trigram)
                ngram_counts[category][trigram] += 1

        self.word_distributions = {category: {} for category in self.categories}
        self.category_weights = {category : self.calculate_category_bias(category_counts[category], ngram_total_count)
                                 for category in self.categories}
        self.vocabulary = vocabulary
        for category in self.categories:
            for ngram in vocabulary:
                self.word_distributions[category][ngram] = \
                    self.calculate_ngram_probability(ngram_counts[category][ngram], ngram_total_count)
        print('Training Finished')

    def calculate_ngram_probability(self, ngram_count, total_ngram_count):
        return (ngram_count + self.mu * (1 / len(self.vocabulary))) / (total_ngram_count + self.mu)

    def calculate_category_bias(self, num_category_documents, num_total_documents):
        return (num_category_documents + self.delta) / (num_total_documents + len(self.categories) * self.delta)

