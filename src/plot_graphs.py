# Adapted from:
# https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

import read_bibtex
import os, shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import gensim

result_dir="doc_results_all_500_30"
model_dir="model_all_500_30"
graph_dir="graph_500_30"
top_dir="top_500_30"
year_from=1980
n_topics=30

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

def main():
    if graph_dir in os.listdir("."): shutil.rmtree("./"+graph_dir)
    os.mkdir("./"+graph_dir)

    # Loading the LDA model
    ldamodel = Lda.load("./"+model_dir+"/all")

    doc_set = read_bibtex.get_bibtex_entries_from(int(year_from))
    
    # # Load results
    dist_array = np.load("./"+result_dir+"/all.npy")
    # transpose_array = np.load("./"+result_dir+"/all_transpose.npy")
    year_list = [int(year) for year in read_bibtex.get_years()]
    year_list.sort()
    year_frac = np.zeros([n_topics, len(year_list)])
    
    # Convert to per topic year weight list
    for doc_no in range(len(dist_array)):
        for topic_no, weight in dist_array[doc_no]:
            year_frac[topic_no][int(doc_set[doc_no]["year"])-year_list[0]] += weight

    year_frac = year_frac / np.sum(year_frac, axis=0)

    ## Plot trend lines per topic
    for topic_no in range(n_topics):
        plt.plot(year_list, 100.0 * year_frac[topic_no])
        plt.xlabel("Year")
        plt.ylabel("Percentage of papers")
        plt.savefig("./"+graph_dir+"/"+str(topic_no)+".pdf")
        plt.clf()

    # # Code to print top papers per topic
    # if graph_dir in os.listdir("."): shutil.rmtree("./"+top_dir)
    # os.mkdir("./"+top_dir)
    # doc_set = read_bibtex.get_bibtex_entries_from(int(year_from))
    # print(len(doc_set))
    # for itr in range(30):
    #     with open("./"+top_dir+"/"+str(itr)+".txt", 'w') as f:
    #         for ind ,_ in transpose_array[itr][0:10]:
    #             f.write(read_bibtex.bibtex_tostring_single(doc_set[ind]).encode("utf-8"))
    #             f.write("\n")
    #             f.write("\n")

    ## Plot frequency histogram
    data = [float(len(x)) for x in dist_array]
    data.sort()
    counter=collections.Counter(data)
    print(data[0])
    print(data[-1])
    plt.bar(counter.keys(),counter.values())

    for itr in counter:
        if counter[itr] < 10:
            plt.text(x = itr , y = counter[itr]+0.15, s = str(counter[itr]), size = 6)    
        elif counter[itr] <100:
            plt.text(x = itr-0.25 , y = counter[itr]+0.15, s = str(counter[itr]), size = 6)
        elif counter[itr] < 1000:
            plt.text(x = itr-0.3 , y = counter[itr]+0.15, s = str(counter[itr]), size = 6)
        else:
            plt.text(x = itr-0.4 , y = counter[itr]+0.15, s = str(counter[itr]), size = 6)

    plt.xlabel("number of topics")
    plt.ylabel("number of documents")
    plt.savefig("./"+graph_dir+"/topic_number.pdf")

main()