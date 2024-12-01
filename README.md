# Pylit

This repo holds a set of Python classes and functions which streamlines text manipulation and analyis.

A Document object is created from a text string.  When instructed to create sentences, each Document is comprised of Sentence objects with various functionality.

By creating the Documents, users can easily see summary information about a text, such as word count, most common words, number of sentences, sentence part of speech structure, and a sentiment score.

# Sentiment

When a sentence is created, the NLTK SentimentIntensityAnalyzer calculates a sentiment score between -1 (negative sentiment) and 1 (positive sentiment).

The document class has cummulative_sentiment method which stores the cummulative sentiment score at the moment of each sentence. This list is used in the plot_cummulative_sentiment method, which is a smoothed curve of cummulative sentiment from first sentence to the last of the document. 
