# Import libraries
from text_preprocessor import TextPreprocessor
from visualizations import Visualizations
from exceptions import ParseException


class NLPLibrary:
    def __init__(self):
        """Initialize NLPLibrary"""
        # Dictionaries to store the following:
        self.data = {
            "word_count": {},
            "word_length": {},
            "sentiment": {},
            "clean_text": {}
        }
        # List to store stop words
        self.stop_words = []
        # Initialize TextPreprocessor
        self.preprocessor = TextPreprocessor()

    def load_text(self, filename, label="", parser=None):
        """ Load text from file, preprocess it, and store relevant data.
            Args:
                filename (str): The path to the text file.
                label (str): A label for the text file.
                parser (function, optional): A custom parsing function. Defaults to None.
            Returns:
                None
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()

            if parser:
                cleaned_text = parser(text)
            else:
                cleaned_text = self.preprocessor.preprocess_text(text)

            self.data["clean_text"][label] = cleaned_text
            self.data["word_count"][label] = self.preprocessor.count_words(cleaned_text)
            self.data["word_length"][label] = self.preprocessor.calculate_word_length(cleaned_text)
            self.data["sentiment"][label] = self.preprocessor.analyze_sentiment(cleaned_text)

        except FileNotFoundError:
            raise ParseException(f"File not found: {filename}")
        except Exception as e:
            raise ParseException(f"Error parsing file: {filename}. {str(e)}")

    def load_stop_words(self, stopfile):
        """ Load stop words from file.
            Args:
                stopfile (str): The path to the stop words file.
            Returns:
                None
        """
        with open(stopfile, 'r', encoding='utf-8') as file:
            self.stop_words = file.read().split(',')
        with open(stopfile, 'r', encoding='utf-8') as file:
            self.stop_words = file.read().split(',')

    def wordcount_sankey(self, word_list=None, k=5):
        """ Generate a Sankey diagram of word frequencies.
            Args:
                word_list (list, optional): A list of words for the Sankey diagram. Defaults to None.
                k (int, optional): The number of top words to consider. Defaults to 5.
            Returns:
                None
        """
        if word_list is None:
            word_list = self.get_top_words(k)

        visualizer = Visualizations(self.data, self.stop_words)
        visualizer.wordcount_sankey(word_list)

    def word_cloud_subplots(self):
        """ Generate subplots of word clouds.
            Returns:
                None
        """
        visualizer = Visualizations(self.data, self.stop_words)
        visualizer.word_cloud_subplots()

    def word_frequency_overlay(self):
        """ Generate a bar plot comparing word frequencies.
            Returns:
                None
        """
        visualizer = Visualizations(self.data, self.stop_words)
        visualizer.word_frequency_overlay()

    def get_top_words(self, k):
        """ Get top words from word count data.
           Args:
               k (int): The number of top words to consider.
           Returns:
               list: A list of top words.
       """
        # Initialize set to store words
        top_words = set()

        # Iterate & extract words with high frequency that are not in stop word and store in set
        for label in self.data["word_count"].keys():
            words = [word for word, count in self.data["word_count"][label].most_common(k) if word not in self.stop_words]
            top_words.update(words)
        return list(top_words)
