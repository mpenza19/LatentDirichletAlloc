# Adapted from:
# https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

import read_bibtex
import os, shutil
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
import gensim
from gensim import corpora
from gensim.test.utils import datapath
import numpy as np

stop = set(stopwords.words('english'))
stop.add("exist")
stop.add("because")
stop.add("via")
stop.add("interest")
stop.add("therefore")
stop.add("hence")
stop.add("this")


exclude = set(string.punctuation)
exclude.add("-")
exclude.add("_")
exclude.add(".")
exclude.add(";")

lemma = WordNetLemmatizer()
stemmer = PorterStemmer()
ntopics = 30
npasses = 400
result_dir="doc_results_all_500_30"
model_dir="model_all_500_30"
year_from=1980

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

def clean(doc):
    punc_free = ''.join(ch for ch in doc if ch not in exclude)
    lemmatized = " ".join(lemma.lemmatize(word)+" " for word in punc_free.lower().split())
    stemmed = " ".join(stemmer.stem(word) for word in lemmatized.split())
    stop_free = " ".join([i for i in stemmed.split() if i not in stop])
    return stop_free

def main():
    if result_dir in os.listdir("."): shutil.rmtree("./"+result_dir)
    os.mkdir("./"+result_dir)

    # Read and clean data
    doc_set = read_bibtex.bibtex_tostring_from(year_from)
    doc_clean = [clean(doc).split() for doc in doc_set]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Loading the LDA model
    ldamodel = Lda.load("./"+model_dir+"/all")

    # Infer topic distribution for each doc
    topic_dist = [ldamodel.get_document_topics(dictionary.doc2bow(doc)) for doc in doc_clean]
    
    # Save results
    np.save("./"+result_dir+"/all", np.array(topic_dist)) 

    dist_array = np.array(topic_dist)
    transpose_array = [[] for x in range(n_topics)]
    for itr in range(len(dist_array)):
        for top, weight in dist_array[itr]:
            transpose_array[top].append((itr, weight))

    for row in transpose_array:
        row.sort(key=lambda x: x[1], reverse=True)
    np.save("./"+result_dir+"/all_transpose", np.array(transpose_array))    

main()