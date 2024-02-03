from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.tokenize import sent_tokenize
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentiment import calculate_sentence_sentiment


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

    sentence_strings = [sentence.sentence_string for sentence in list_of_sentences]
    
    cv = CountVectorizer(stop_words="english")
    cv_sentences = np.array(cv.fit_transform(sentence_strings).todense())

    for sentence, cv_sentence in zip(list_of_sentences, cv_sentences):
        sentence.cv_sentence = cv_sentence

    return cv_sentences


def find_most_similar_sentence(
    target_sentence,
    list_of_sentences
):

    # make a list of all count vectorized forms of a sentence
    cv_sentences = [sentence.cv_sentence for sentence in list_of_sentences]
    
    # define an array of cosine similarities of all sentences compared to a target sentence
    sentence_similarities = cosine_similarity(
        cv_sentences, [target_sentence.cv_sentence]
    )

    highest_similarity_score = 0
    highest_similarity_index = 0
    for i, similarity_score in enumerate(sentence_similarities):
        # A similarity score of 1 means it is most likely the same sentence
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
        self.cv_sentence = []
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
        if self.punctuation_marks[-1] in sentence_types:
            self.type_of_sentence = sentence_types[self.punctuation_marks[-1]]
        else:
            self.sentence_type = "undefined"
    