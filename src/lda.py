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
npasses = 500
result_dir="results_all_500_30"
model_dir="model_all_500_30"
year_from=1980

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# A function to clean the text of punctuation and stopwords. It also reduces related words to their root
def clean(doc):
    punc_free = ''.join(ch for ch in doc if ch not in exclude)
    lemmatized = " ".join(lemma.lemmatize(word)+" " for word in punc_free.lower().split())
    stemmed = " ".join(stemmer.stem(word) for word in lemmatized.split())
    stop_free = " ".join([i for i in stemmed.split() if i not in stop])

    return stop_free

def main():
    if result_dir in os.listdir("."): shutil.rmtree("./"+result_dir)
    os.mkdir("./"+result_dir)

    if model_dir in os.listdir("."): shutil.rmtree("./"+model_dir)
    os.mkdir("./"+model_dir)

    doc_set = read_bibtex.bibtex_tostring_from(year_from)
    doc_clean = [clean(doc).split() for doc in doc_set]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=ntopics, id2word = dictionary, passes=npasses, random_state=0)

    # Saving the LDA model
    ldamodel.save("./"+model_dir+"/all")

    # Write results
    with open("./"+result_dir+"/all_results.txt", 'w') as f:
        for topic in ldamodel.print_topics(num_topics=ntopics, num_words=10):
            f.write("#%i: %s\n" % topic)

main()