import os
from pathlib import Path
import sys
from nltk.tokenize import word_tokenize, RegexpTokenizer

import sys

repo_name = "pylit"
base_path = (__file__).split(repo_name)[0] + "/" + repo_name
sys.path.append(base_path)
from file_metadata import find_directory_files, sort_files_by_modified_date, count_words_in_file

from documents import Document

files = find_directory_files("/Users/mbarry/Documents/03_hobbies/")
modified_files = sort_files_by_modified_date(files)[:20]

documents = []
for found_file in modified_files:
    doc = Document(found_file[1], create_sentences=True)
    documents.append(doc)
    doc.find_longest_sentence()
    print(doc.longest_sentence)



test_doc = Document(modified_files[1][1])


print(test_doc.word_count)
test_doc.sentences
test_doc.sentence_count
test_doc.cumulative_sentiment()
test_doc.find_longest_sentence()
test_doc.describe()


