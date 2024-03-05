import sys

repo_name = "pylit"
base_path = (__file__).split(repo_name)[0] + "/" + repo_name
sys.path.append(base_path)

from sentences import Sentence
from sentences import tfidf_vectorize_sentences, count_vectorize_sentences, find_sentences, find_most_similar_sentence

from documents import Document

with open("../sample_data/sample_journal.txt", "r") as read_file:
    sample_journal = read_file.read()

journal = Document("../sample_data/sample_journal.txt")

journal.plot_cumulative_sentiment()

sentiment = [s.sentiment_score for s in journal.sentences]
