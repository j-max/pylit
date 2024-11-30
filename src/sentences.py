from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.tokenize import sent_tokenize
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentiment import calculate_sentence_sentiment
from nltk.corpus import stopwords




def find_sentences(document_string):

    """Given a document sting, return a list of sentences
    :parameters: document string: a document represented as a text string
    :return: a list of sentences
    :rtype: list
    """
    # TODO Figure out how to parse the date stamps of a journal entry
    tokenized_sentences = sent_tokenize(document_string)
    sentences = [Sentence(sentence_string) for sentence_string in tokenized_sentences]
    
    return sentences


def count_vectorize_sentences(list_of_sentences):

    """Take a list of Sentence objects and count vectorizee them

    :Paramaters: a list of Sentence objects
    :return: the fit countvectorizer and an array of vectorized sentences
    :rtype: tuple
    """

    sentence_strings = [sentence.sentence_string for sentence in list_of_sentences]
    
    cv = CountVectorizer(stop_words="english")
    cv_sentences = np.array(cv.fit_transform(sentence_strings).todense())

    for sentence, vector in zip(list_of_sentences, cv_sentences):
        sentence.sentence_vector = vector

    return cv, cv_sentences


def tfidf_vectorize_sentences(list_of_sentences):

    """Given a list of sentence objects, tfidf vectorise the sentences

    :return: the fit vectorizer and the a numpy array of vectors
    :rtype: tuple
    """

    sentence_strings = [sentence.sentence_string for sentence in list_of_sentences]
    
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_sentences = np.array(tfidf.fit_transform(sentence_strings).todense())

    for sentence, vector in zip(list_of_sentences, tfidf_sentences):
        sentence.sentence_vector = vector

    return tfidf, tfidf_sentences


def find_most_similar_sentence(
    target_sentence,
    list_of_sentences
):
    
    # make a list of all count vectorized forms of a sentence
    vector_sentences = [sentence.sentence_vector for sentence in list_of_sentences]
    
    # define an array of cosine similarities of all sentences compared to a target sentence
    sentence_similarities = cosine_similarity(
        vector_sentences, [target_sentence.sentence_vector]
    )

    highest_similarity_score = 0
    highest_similarity_index = 0
    for i, similarity_score in enumerate(sentence_similarities):
        # A similarity score of .9999 means it is most likely the same sentence
        # there could be sentences with the same words in a different order.
        if similarity_score[0] <= .999999 and similarity_score > highest_similarity_score:
            highest_similarity_score = similarity_score
            highest_similarity_index = i
    
    print(highest_similarity_score)
    print(highest_similarity_index)

    return list_of_sentences[highest_similarity_index].sentence_string


class Sentence:

    """
    The Sentence is the foundational on which the subsequent classes are built.
    Sentences are broken up into tokens. 

    Each sentence has a sentiment score determined by NLTK VADER.

    Take a sentence string and describe it:
        Length
        Number of words
        Type of sentence based on punctuation

    """

    def __init__(self, sentence_string):
        
        self.sentence_string = sentence_string
        self.word_tokens = []
        self.word_tokenize()
        self.punctuation_marks = []
        self.find_punctuation_marks()
        self.type_of_sentence = ""
        self.determine_type_of_sentence()
        self.string_length = len(self.sentence_string)
        self.word_count = len(self.word_tokens)
        self.sentiment_score = calculate_sentence_sentiment(self.sentence_string)
        self.date = ''
        self.sentence_vector = []
        # TODO Add timestamps to journal sentences
        # TODO Add POS to the tokens
        
    
    def word_tokenize(self):
        
        tokenizer = RegexpTokenizer(r"\w+")
        self.word_tokens = tokenizer.tokenize(self.sentence_string)

    
    def find_punctuation_marks(self):

        # find elipses first, so that the match doesn"t stop after a period
        tokenizer = RegexpTokenizer(r"\.{3}|[!,;:?.]")
        self.punctuation_marks = tokenizer.tokenize(self.sentence_string)
        
    
    def determine_type_of_sentence(self):

        sentence_types = {
            ".": "declarative",
            "?": "question",
            "!": "exclamation"}
        
        # determine the sentence type by the last punctuation token
        try:
            if self.punctuation_marks[-1] in sentence_types:
                self.type_of_sentence = sentence_types[self.punctuation_marks[-1]]
            else:
                self.sentence_type = "undefined"
        except IndexError:
            self.sentence_string = "undefined"
            
    def remove_stopwords(self):
        """
        Remove stopwords from the sentence tokens.  
        This will replace the original sentence tokens
        with a list with stopwords removed. 

        """
        no_stop_tokens = [word for word in self.word_tokens if word.lower() not in stopwords.words('english')]

        self.word_tokens = no_stop_tokens


