# Import the libraries
import re
import string
from collections import Counter


class TextPreprocessor:
    def preprocess_text(self, text):
        """ Cleaning the data.
            Args:
                text (str): The input text to be preprocessed.
            Returns:
                str: The preprocessed text
        """
        # Remove punctuation and convert to lowercase
        text = text.translate(str.maketrans("", "", string.punctuation)).lower()
        # Remove quotation marks
        text = text.replace('"', '').replace("'", '')
        text = text.replace('“', '').replace("”", '')
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def count_words(self, text):
        """ Counts the occurrences of each unique word in the input text.
            Args:
                text (str): The input text to count words from.
            Returns:
                collections.Counter: A Counter object containing the count of each unique word.
        """
        # Split the text & count occurrences
        words = text.split()
        word_count = Counter(words)
        return word_count

    def calculate_word_length(self, text):
        """ Calculates the average word length of the words in the input text.
            Args:
                text (str): The input text to calculate the average word length from.
            Returns:
                float: The average word length.
        """
        # Split the text, count the length & store them in a list
        words = text.split()
        word_lengths = [len(word) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths)
        return avg_word_length

    def analyze_sentiment(self, text):
        """ Analyzes the sentiment of the input text.
            Args:
                text (str): The input text to perform sentiment analysis on.
            Returns:
                float: A placeholder value indicating the sentiment score.
        """
        # Placeholder for sentiment analysis - indicating neutral sentiment
        return 0.5
