# Adapted from:
# https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

import read_bibtex
import os, shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import gensim

# import seaborn

result_dir="doc_results_all_500_30"
model_dir="model_all_500_30"
graph_dir="graph_500_30"
top_dir="top_500_30"
year_from=1980

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
    
    # exit(0)

def main():
    if result_dir in os.listdir("."): shutil.rmtree("./"+result_dir)
    os.mkdir("./"+result_dir)

    p = mp.Pool(processes=8)
    p.map(check_results, read_bibtex.get_years())
    p.close()

def main2():
    # if graph_dir in os.listdir("."): shutil.rmtree("./"+graph_dir)
    # os.mkdir("./"+graph_dir)

    # Loading the LDA model
    ldamodel = Lda.load("./"+model_dir+"/all")

    # Infer topic distribution for each doc
    # topic_dist = [ldamodel.get_document_topics(dictionary.doc2bow(doc)) for doc in doc_clean]
    
    # Load results
    dist_array = np.load("./"+result_dir+"/all.npy")
    transpose_array = np.load("./"+result_dir+"/all_transpose.npy")
    print(min([max(row, key=lambda x: x[1]) for row in dist_array], key=lambda x: x[1]))

    doc_set = read_bibtex.get_bibtex_entries_from(int(year_from))

    for itr in range(30):
        with open("./"+top_dir+"/"+str(itr)+".txt", 'w') as f:
            for ind ,_ in transpose_array[itr][0:10]:
                f.write(str(doc_set[ind]))
                f.write("\n")

    # for itr in range(len(dist_array)):
    #     for top, weight in dist_array[itr]:
    #         transpose_array[top].append((itr, weight))

    # for row in transpose_array:
    #     row.sort(key=lambda x: x[1], reverse=True)

    # np.save("./"+result_dir+"/all_transpose", np.array(transpose_array))
    
    data = np.array([float(len(x)) for x in dist_array])
    d = np.diff(np.unique(data)).min()
    left_of_first_bin = data.min() - float(d)/2
    right_of_last_bin = data.max() + float(d)/2

    plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d, d)) #,normed=True, bins=30
    plt.xlabel("number of topics")
    plt.xlabel("number of documents")
    plt.savefig("./"+graph_dir+"/topic_number.pdf")

# check_results("2016")
main2()