import dateutil.parser as dparser
from pathlib import Path
import re

from nltk.corpus import stopwords
from nltk.probability import FreqDist
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sentences import Sentence
from sentences import find_sentences


class Document:

    def __init__(
        self,
        read_in_file=True,
        path_to_document="",
        document_string="",
        create_sentences=True
    ):

        # TODO Add document title -> add to plots as well
        self.path_to_document = path_to_document
        self.document_name = ""
        self.document_string = ""
        if read_in_file:
            self.read_in_document()
        else:
            self.document_string = document_string
        # Creating sentences makes each sentence a Sentence object
        # which means a long runtime
        if create_sentences:
            self.sentences = find_sentences(self.document_string)
            self.sentence_count = len(self.sentences)
            self.word_count = self.count_words()
            self.avg_sentiment = float(np.mean([sentence.sentiment_score for sentence in self.sentences]))
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

        return self.longest_sentence
    
    def find_most_common_word(self):

        all_tokens = []
        
        for sentence in self.sentences:
            all_tokens.extend(sentence.word_tokens)

        # Make words lowercase to allow for correct token counting
        all_tokens = [token.lower() for token in all_tokens]
        fd = FreqDist(all_tokens)

        self.most_frequent_word = fd.max()
        
        return self.most_frequent_word

    def count_questions(self):

        question_count = 0
        for sentence in self.sentences:
            if sentence.type_of_sentence == "question":
                question_count += 1
        
        self.question_count = question_count
        
        return self.question_count
    
    def remove_stop_words(
        self,
        replace_document_string=False
    ):
    
        """
        remove stop words from all sentences.
        
        If replace_document_string=True
        The original document string will be replace with a string
        that has no stopwords.
        """
        
        no_stop_document_tokens = []
        for sentence in self.sentences:
            sentence.remove_stopwords()
            if replace_document_string:
                no_stop_document_tokens.extend(sentence.word_tokens)
        
        if replace_document_string:
            self.document_string = " ".join(no_stop_document_tokens)
            self.word_count = self.count_words()

    def pos_tag_sentences(self):

        for sentence in self.sentences:
            sentence.pos_tag()

    def describe(self):

        descriptions = {
            "doc_name": [self.document_name],
            "word_count": [self.word_count],
            "sentence_count": [self.sentence_count],
            "longest_sentence": [self.find_longest_sentence()],
            "most_common_word": [self.find_most_common_word()],
            "question_count": [self.count_questions()],
            "avg sentiment": [self.avg_sentiment]
        }
    
        # create a dataframe to allow for nice head() output
        df = pd.DataFrame(descriptions)
        print(df.head())

        # Return dictionary to allow for concatenation of data in corpus
        return descriptions
    
