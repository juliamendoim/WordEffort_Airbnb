import os 
import codecs
from nltk import sent_tokenize as st

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

textos = './Airbnb_txt/'

corpus = []

for comentario in os.listdir(textos):
	archivo = codecs.open(textos+comentario, 'r', encoding = 'utf-8')
	comentario = archivo.read()
	sentences = st(comentario)
	for oracion in sentences:
		corpus.append(oracion)


vectorizer = TfidfVectorizer()

kmeans = KMeans(n_clusters=150)

matriz = vectorizer.fit_transform(corpus)

kmeans.fit(matriz)

clusters = [[corpus[i],kmeans.labels_[i]] for i in range(len(corpus))]
clusters = pd.DataFrame(clusters)
#clusters = clusters.sort_values(1)


#chicho = vectorizer.inverse_transform(pipo)

clusters.to_csv('./clusters150.csv','*', encoding = 'utf-8')



#guardar desde Sublime como utf8 with BOM y reemplazar las ',' por ';' para ver en Excel