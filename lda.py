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
import multiprocessing as mp

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
stemmer = PorterStemmer()
ntopics = 20
npasses = 100

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    lemmatized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    stemmed = " ".join(stemmer.stem(word) for word in lemmatized.split())
    return stemmed

def train_model(year_dir):
    # Read and clean data
    doc_set = read_bibtex.bibtex_tostring_year(year_dir)
    doc_clean = [clean(doc).split() for doc in doc_set]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=ntopics, id2word = dictionary, passes=npasses)

    # Write results
    with open("./results/"+year_dir+".txt", 'w') as f:
        for topic in ldamodel.print_topics(num_topics=ntopics, num_words=5):
            f.write("#%i: %s\n" % topic)
        print year_dir

def main():
    if "results" in os.listdir("."): shutil.rmtree("./results")
    os.mkdir("./results")

    p = mp.Pool(processes=8)
    p.map(train_model, read_bibtex.get_years())
    p.close()

#train_model("2005")
main()