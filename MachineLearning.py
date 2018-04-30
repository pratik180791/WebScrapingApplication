from __future__ import print_function
from Home import connectDB
import nltk
import numpy as np
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import codecs
from sklearn import feature_extraction
import mpld3
#nltk.download()

cursor_data=connectDB()

title_p=[]
date_p=[]
for document in cursor_data:
    title_p .append(document["title"])
    date_p.append(str((document['date'])))

#print(title_p[:10])
noise_list = ["is", "a", "this", "..."]

stopwords = nltk.corpus.stopwords.words('english')
#print(stopwords[:10])
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

totalvocab_stemmed = []
totalvocab_tokenized = []

def ml_task():
    for i in title_p:
        allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)

    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)

    tfidf_vectorizer = TfidfVectorizer(max_df=1.1, max_features=200000,min_df=0.01, stop_words='english',use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(title_p) #fit the vectorizer to synopses
    terms = tfidf_vectorizer.get_feature_names()

    from sklearn.metrics.pairwise import cosine_similarity
    dist = 1 - cosine_similarity(tfidf_matrix)
    from sklearn.cluster import KMeans
    num_clusters = 3
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)

    clusters = km.labels_.tolist()

    print("Top terms per cluster:")
    print()
    # sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    results = ""
    for i in range(num_clusters):

        print("Cluster %d words:" % i, end='')
        cluster_info_1="Cluster %d words:"%(i)
        for ind in order_centroids[i, :5]:  # replace 6 with n words per cluster
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
            temp=str(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))+" "
            cluster_info_1+= temp

        cluster_info_1+=temp
        print()  # add whitespace
        print()  # add whitespace
    cluster_info_1 += "\n"
    cluster_info_1 += "\n"

   # return cluster_info_1


