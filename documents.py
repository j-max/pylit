from pathlib import Path

from nltk.corpus import stopwords

import pandas as pd
import re
import dateutil.parser as dparser

import matplotlib.pyplot as plt
import seaborn as sns

from sentences import Sentence
from sentences import find_sentences


class Document:

    def __init__(
        self,
        path_to_document,
        create_sentences=True
    ):

        # TODO Add document title -> add to plots as well
        self.path_to_document = path_to_document
        self.document_name = ""
        self.document_string = ""
        self.read_in_document()
        # Creating sentences makes each sentence a Sentence object
        # which means a long runtime
        if create_sentences:
            self.sentences = find_sentences(self.document_string)
            self.sentence_count = len(self.sentences)
            self.word_count = self.count_words()
        else:
            self.sentences = None
            self.sentence_count = None
            self.word_count = None

        self.longest_sentence = None
        # TODO add most frequent sentence construction
        # TODO add counts of different types of words

    def read_in_document(self):
        
        """
        Read in a document given a path to the document
        """
        
        # create Path object to allow access to document name
        doc_path = Path(self.path_to_document)

        with open(Path(doc_path), "r") as read_file:
            self.document_string = read_file.read().replace("\n", " ")
            self.document_name = doc_path.name
                   

    def find_document_sentences(self):

        # TODO Figure out how to parse the date stamps of a journal entry
        self.sentences = find_sentences(self.document_string)
        self.sentence_count = len(self.sentences)
        

    def cumulative_word_count(self):
        """Take a list of sentences, and count new words cumulatively.
 
        The cumulative_word_count() function returns a list which 
        counts the number of new words added as the document grows.  

        The larger the document, the smaller the slope will be, since 
        it is a higher probabilty that each successive word added will
        have been already used in the document.

        The changes in the slope of the graph may give a sense of
        where new ideas are introduced.           

        :param sentence_list: _description_
        :type sentence_list: list
        :return: a list of the cumulative count
        :rtype: list
        """

        # Put all sentence word tokens into one list
        ordered_sentence_tokens = []
        for sentence in self.sentences:
            ordered_sentence_tokens.extend(sentence.word_tokens)
        
        used_words_list = []
        cumulative_count = 0
        cumulative_count_array = []
        for token in ordered_sentence_tokens:
            if token not in used_words_list:
                used_words_list.append(token)
                cumulative_count+=1
            cumulative_count_array.append(cumulative_count)
        
        return cumulative_count_array
    
    def cumulative_sentiment(self) -> list:
        """
        Create an array of values represented the sentiment of document sentences"

        :return: a list of VADER sentiment scores for each sentence
        :rtype: list
        """
        
        cumulative_sentiment = 0
        sentiment_array = []

        for sentence in self.sentences:
            cumulative_sentiment+=sentence.sentiment_score
            sentiment_array.append(cumulative_sentiment)

        return sentiment_array
    
    def plot_cumulative_sentiment(
        self,
        rolling_window=7,
        plot_title="Cumulative Sentiment of the Document",
        x_label="Sentence index",
        y_label="Cumulative Sentiment"
    
    ):
        """Plot the cumulative sentiment of a document

        :param rolling_window: increase the window to smooth out the graph, defaults to 7
        :type rolling_window: int, optional
        :param plot_title: defaults to "Cumulative Sentiment of the Document"
        :type plot_title: str, optional
        :param x_label: defaults to "Sentence index"
        :type x_label: str, optional
        :param y_label: defaults to "Cumulative Sentiment"
        :type y_label: str, optional
        """

        # Transform list to series to allow for rolling function
        sentiment = pd.Series(self.cumulative_sentiment())
        smoothed_sentiment = sentiment.rolling(rolling_window).mean()

        fig, ax = plt.subplots()

        sns.lineplot(smoothed_sentiment)

        ax.set_title(plot_title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)


    def count_words(self):

        all_tokens = []

        for sentence in self.sentences:
            all_tokens.extend(sentence.word_tokens)

        return len(all_tokens)
    
    def date_sentences(self):
        last_date = ''
        for sentence in self.sentences:
            try:
                sentence.date = dparser.parse(sentence.sentence_string, fuzzy=True)
                last_date = sentence.date
            except:
                print(sentence)
                self.date = last_date
    
    def find_longest_sentence(self):

        """Find the longest sentence string amongst 
        all sentence objects in a document"""

        longest_sentence_length = 0
        longest_sentence_string = ""
        for sentence in self.sentences:
            if len(sentence.sentence_string) > len(longest_sentence_string):
                longest_sentence_length = len(sentence.sentence_string)
                longest_sentence_string = sentence.sentence_string

        self.longest_sentence = longest_sentence_string
    
    def describe(self):

        print(
            f"""
            Document Name: {self.document_name}
            Word count: {self.word_count}
            Sentence count: {self.sentence_count}
            Longest sentence: {self.longest_sentence}
            """
        )

