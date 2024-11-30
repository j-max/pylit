from file_metadata import find_directory_files
from documents import Document

class Corpus:

    def __init__(
        self,
        path_to_documents_folder, 
        create_sentences=True
    ):

        self.path_to_documents_folder = path_to_documents_folder
        self.documents = []
        self.document_count = 0
        self.read_in_documents(create_sentences=create_sentences)
        self.corpus_string = self.create_corpus_string()
        self.word_count = 0
        self.count_corpus_words()
        self.document_tokens = []
        

    def read_in_documents(
        self,
        create_sentences,
        doctype="txt"
    ):

        """ 
        Read in all documents of the given doctype
        and store them in the document dicionary
        """
        
        document_paths = find_directory_files(self.path_to_documents_folder)
        for doc_path in document_paths:
            self.documents.append(
                Document(
                    doc_path, 
                    create_sentences=create_sentences
                )
            )

        self.document_count = len(self.documents)
        print(f"There are {self.document_count} documents in the corpus")
        return self.documents
    

    def create_corpus_string(self):
        
        """
        Create 1 long string of all document text
        """

        corpus_string = ""
        for document in self.documents:
            corpus_string += document.document_string

        return corpus_string


    def tokenize_corpus(self, remove_stop_words=False):
        
        """
        Create a set of word tokens from
        the corpus string
        """

        # Use Regex tokenizer to remove numbers and punctuation.
        tokenizer = RegexpTokenizer(r"\w+")
        tokenized_words = tokenizer.tokenize(self.corpus_string)
        tokenized_words = [word.lower() for word in tokenized_words]

        if remove_stop_words:
            tokenized_words = [
                word for word in tokenized_words 
                if word not in stopwords.words("English")
            ]
            self.document_tokens = tokenized_words
            return tokenized_words
        
        else:
            self.document_tokens = tokenized_words
            return tokenized_words

    def count_corpus_words(self):
        word_count = 0
        for document in self.documents:
            word_count += document.word_count

        self.word_count = word_count

    def find_longest_document(self):

        longest_doc_length = 0
        longest_doc_name = ""
        for document in self.documents:
            if document.word_count > longest_doc_length:
                longest_doc_length = document.word_count
                longest_doc_name = document.document_name
        print("The longest document is: ", longest_doc_name, str(longest_doc_length))
        return longest_doc_name, longest_doc_length


