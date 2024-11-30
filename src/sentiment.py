from nltk.sentiment import SentimentIntensityAnalyzer


def calculate_sentence_sentiment(sentence_string):
    """
    Use NLTK's VADER to score sentence sentiment.

    VADER returns a dictionary, ex:
    {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}
    Compound is
    """

    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(sentence_string)

    return sentiment_score["compound"]


def fetch_most_positive_sentence(sentence_list):

    sentence_list = [
        (sentence.sentiment_score, sentence.sentence_string) 
        for sentence in sentence_list
    ]

    sentence_list.sort(reverse=True)

    return sentence_list[0]


def order_sentences_by_sentiment(sentence_list):

    sentence_list = [
        (sentence.sentiment_score, sentence.sentence_string) 
        for sentence in sentence_list
    ]

    sentence_list.sort(reverse=True)

    return sentence_list


def find_10_most_positive(sentence_list):
    top_sentiment_score = 0
    top_sentiment_index = 0
    for i in range(0, len(sentence_list)-10):

        sentences = sentence_list[i: i+10]

        sentiment_for_range = sum(
            [sentence.sentiment_score for sentence in sentences]
        )
        print(sentiment_for_range)
        if sentiment_for_range > top_sentiment_score:
            top_sentiment_score = sentiment_for_range
            top_sentiment_index = i

    print(top_sentiment_score)
    print(top_sentiment_index)
    top_sentences = sentence_list[top_sentiment_index: top_sentiment_index+10]

    return top_sentences