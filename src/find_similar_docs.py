# Adapted from:
# https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

import read_bibtex
import os, shutil, sys
import numpy as np
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
import gensim
from gensim import corpora
from gensim.test.utils import datapath


result_dir="doc_results_all_500_30"
model_dir="model_all_500_30"
year_from=1980
n_topics=30

stop = set(stopwords.words('english'))
stop.add("exist")
stop.add("because")
stop.add("via")
stop.add("interest")
stop.add("therefore")
stop.add("hence")
stop.add("this")

lemma = WordNetLemmatizer()
stemmer = PorterStemmer()
exclude = set(string.punctuation)
exclude.add("-")
exclude.add("_")
exclude.add(".")
exclude.add(";")


# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

def clean(doc):
    punc_free = ''.join(ch for ch in doc if ch not in exclude)
    lemmatized = " ".join(lemma.lemmatize(word)+" " for word in punc_free.lower().split())
    stemmed = " ".join(stemmer.stem(word) for word in lemmatized.split())
    stop_free = " ".join([i for i in stemmed.split() if i not in stop])
    return stop_free

def main():
    doc_set = read_bibtex.bibtex_tostring_from(year_from)
    doc_clean = [clean(doc).split() for doc in doc_set]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Loading the LDA model
    ldamodel = Lda.load("./"+model_dir+"/all")

    # Load results
    dist_array = np.load("./"+result_dir+"/all.npy")
    # transpose_array = np.load("./"+result_dir+"/all_transpose.npy")
    
    # Convert dist_array from a list of tupules to an actual matrix
    dist_matrix = np.zeros([len(dist_array), n_topics])
    for itr in range(len(dist_array)):
        for top, weight in dist_array[itr]:
            dist_matrix[itr][top] = weight

    # Read file given as a command line argument
    text_read = []
    with open(sys.argv[1]) as f:
        text_read = f.read()
    text_read = text_read.decode('utf-8')
    topic_list = ldamodel.get_document_topics(dictionary.doc2bow(clean(text_read).split()))
    topic_vector = np.zeros([1,n_topics])
    print(topic_list)
    for top, weight in topic_list:
        topic_vector[0][top] = weight

    # Find distance of topic vectors
    distances = [(itr, np.sum(np.abs(row-topic_vector))) for row, itr in zip(dist_matrix, range(len(dist_matrix)))]
    distances.sort(key=lambda x: x[1])

    # Print title of closest papers
    doc_set = read_bibtex.get_bibtex_entries_from(int(year_from))
    for itr in range(3):
        print(doc_set[distances[itr][0]]["title"])
        print("\n")

main()