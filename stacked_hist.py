import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import gensim
from gensim import corpora
import read_bibtex, lda, compatibility

import numpy as np

init_notebook_mode(connected=True)

run_code = "_500_30"
result_dir="doc_results_all"+run_code
model_dir="model_all"+run_code
graph_dir="graph"+run_code
top_dir="top"+run_code
year = 1991
all_years = read_bibtex.get_years()

Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda.load("./"+model_dir+"/all")



print "loaded"


def get_topic_weights_this_year(yr):
    print yr
    doc_set = read_bibtex.bibtex_tostring_year(str(yr))
    doc_clean = [lda.clean(doc).split() for doc in doc_set]
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    topic_dist = [ldamodel.get_document_topics(dictionary.doc2bow(doc)) for doc in doc_clean]

    topic_weights = dict()
    total_weight = 0
    for row in topic_dist:
        for topic, weight in row:
            total_weight += weight

            if topic not in topic_weights:
                topic_weights[topic] = list()
            topic_weights[topic].append(weight)
    
    topic_weights = dict([(topic, sum(topic_weights[topic]) / total_weight) if topic in topic_weights else (topic, 0.0) for topic in range(ldamodel.num_topics)])
    
    #for topic, weight in topic_weights: print topic, weight
    return topic_weights


def get_topic_weights_by_year():
    weights_by_year = dict([(yr, get_topic_weights_this_year(yr)) for yr in all_years])

    #for yr, topic_weights in weights_by_year.iteritems():
        #print yr
        #for topic, weight in topic_weights.iteritems():
            #print '\t', topic, weight

    return weights_by_year


def get_weights_this_topic_by_year(topic, weights_by_year):
    if topic < 0 or topic >= ldamodel.num_topics:
        sys.stderr.write("ERROR: invalid topic number.\n")
        exit()

    
    
    weight_this_topic_by_year = dict([(year, topic_weights[topic]) for year, topic_weights in weights_by_year.iteritems()])
    
    #for year, weight_this_topic in weight_this_topic_by_year.iteritems():
    #    print year, weight_this_topic

    return weight_this_topic_by_year


def get_weights_by_topic_by_year(weights_by_year):
    weights_by_topic_by_year = dict()
    
    for topic in range(ldamodel.num_topics):
        print topic
        weights_by_topic_by_year[topic] = get_weights_this_topic_by_year(topic, weights_by_year)
        print weights_by_topic_by_year[topic]
        #dict([(topic, get_weights_this_topic_by_year(topic)) ])
    
    for topic, weight_this_topic_by_year in weights_by_topic_by_year.iteritems():
        print "TOPIC %s" % topic
        for year, weight_this_topic in weight_this_topic_by_year.iteritems():
            print "\t%s %s" % (year, str(weight_this_topic))

    return weights_by_topic_by_year


        



weights_by_year = get_topic_weights_by_year()
weight_matrix = get_weights_by_topic_by_year(weights_by_year)
print "matrix formed"

data = [go.Bar(x = all_years, y = weight_matrix[topic].values(), name = ("Topic %s" % topic)) for topic in range(ldamodel.num_topics)]
layout = go.Layout(barmode='stack')
fig = go.Figure(data=data, layout=layout)
plot(fig, filename='stacked-bar', image='jpeg')