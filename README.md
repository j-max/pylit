
# Sentiment

When a sentence is created, the NLTK SentimentIntensityAnalyzer calculates a sentiment score between -1 (negative sentiment) and 1 (positive sentiment).

The document class has cummulative_sentiment method which stores the cummulative sentiment score at the moment of each sentence. This list is used in the plot_cummulative_sentiment method, which is a smoothed curve of cummulative sentiment from first sentence to the last of the document. 
