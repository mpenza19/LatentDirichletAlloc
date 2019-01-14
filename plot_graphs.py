# Adapted from:
# https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

import read_bibtex
import os, shutil
import string
import gensim
import multiprocessing as mp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# import seaborn

result_dir="doc_results_all"
model_dir="model_all"


# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

def clean(doc):
    punc_free = ''.join(ch for ch in doc if ch not in exclude)
    lemmatized = " ".join(lemma.lemmatize(word)+" " for word in punc_free.lower().split())
    stemmed = " ".join(stemmer.stem(word) for word in lemmatized.split())
    stop_free = " ".join([i for i in stemmed.split() if i not in stop])
    return stop_free

def check_results(year_dir):
    # Read and clean data
    # doc_set = read_bibtex.bibtex_tostring_year(year_dir)
    # doc_clean = [clean(doc).split() for doc in doc_set]

    # # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    # dictionary = corpora.Dictionary(doc_clean)

    # # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    # doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Loading the LDA model
    ldamodel = Lda.load("./"+model_dir+"/"+year_dir)

    # Infer topic distribution for each doc
    # topic_dist = [ldamodel.get_document_topics(dictionary.doc2bow(doc)) for doc in doc_clean]
    
    # Load results
    dist_array = np.load("./"+result_dir+"/"+year_dir+".npy")

    data = np.array([float(len(x)) for x in dist_array])
    d = np.diff(np.unique(data)).min()
    left_of_first_bin = data.min() - float(d)/2
    right_of_last_bin = data.max() + float(d)/2

    plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d, d)) #,normed=True, bins=30
    plt.show()
    # exit(0)

def main():
    if result_dir in os.listdir("."): shutil.rmtree("./"+result_dir)
    os.mkdir("./"+result_dir)

    p = mp.Pool(processes=8)
    p.map(check_results, read_bibtex.get_years())
    p.close()

def main2():
    # if result_dir in os.listdir("."): shutil.rmtree("./"+result_dir)
    # os.mkdir("./"+result_dir)

    # Loading the LDA model
    ldamodel = Lda.load("./"+model_dir+"/all")

    # Infer topic distribution for each doc
    # topic_dist = [ldamodel.get_document_topics(dictionary.doc2bow(doc)) for doc in doc_clean]
    
    # Load results
    dist_array = np.load("./"+result_dir+"/all.npy")

    data = np.array([float(len(x)) for x in dist_array])
    d = np.diff(np.unique(data)).min()
    left_of_first_bin = data.min() - float(d)/2
    right_of_last_bin = data.max() + float(d)/2

    plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d, d)) #,normed=True, bins=30
    plt.show()

# check_results("2016")
main2()