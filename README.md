# LatentDirichletAlloc
A python implementation to apply Latent Dirichlet allocation model on paper abstract and citation data.
This was implemented for COS 561 project in Princeton University.
The code base was used to learn a LDA model on abstract data from the INFOCOM conference and analyse it.

## Requirements
numpy
matplotlib
pyplot
gensim
bibtexreader

## Instructions

They need to be stored in a folder named abstracts which contains a directory for each year of the conference.
Within a year directory a txt file containing the abstract and title data is kept in the form of Bibtex citations.
(We are working on publishing the data we used)

To train the model run the following command:
```
python src/lda.py
 ```
it will train a topic model with 30 topics and store model params in model_all_500_30 and store the list of top words
related to a topic in result_all_500_30. Now we can run various tests on it. If we want to generate the topic distributions
for the dataset run the command:
```
python src/lda_test.py
 ```
it will store the data as a numpy array in the director doc_results_all_500_30. At this point we can use the model to input
abstracts from arbitrary papers (even from other sources) and try to find similar papers. For that run the command:
```
python src/find_similar_docs.py FILE_NAME
 ```
 FILE_NAME should be a text file containing the abstract and title data. This command will print out the topic distribution
 for the data in file and the title of the 3 closest papers on which the model was trained.

To make a stacked bargraph to show trends over the years run the command,
```
python src/stacked_barchart.py
 ```
which will output the image in a file named "topic_weights_by_year.svg". To make the trend line graphs and the frequency histogram run.
```
python src/plot_graphs.py
 ```