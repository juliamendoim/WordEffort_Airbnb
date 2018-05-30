import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import defaultdict
import json

def cluster_in(lista, clusters,name):
    diccionario_pandaFrames = [] #necesito crear una lista con los valores de los clusters
    for i in lista:
        numero = clusters[0] == i[0] # esto indica que si una oracion de la columna 0 es igual a la oracion guardada en pesos, devuelve True
        num_cluster = clusters[numero][1] # aca busca en el row que le dio True un valor del cluster donde estaba esa oracion
        cluster = clusters[1] == int(num_cluster)
        
        diccionario_pandaFrames.append({'name': i[0], 'size' : i[1], 'children' : [{'name' : x, 'size' : 1, 'children' : []}  for x in list(clusters[cluster][0]) if x != i[0]]}) 
        
    resultado = {
      "name":name,
      "children":None
    }
    resultado['children'] =  diccionario_pandaFrames
    return resultado

clustercsv = pd.read_csv('clusters150.csv', sep = '*') #abre un csv con todas las oraciones y su cluster como un dataframe de pandas

def procesar_cluster(numero): 
    cluster_num = clustercsv['1'] == numero  #este snippet elige todas las oraciones de un cluster y devuelve la columna '0' como texto 
    cluster_num = clustercsv[cluster_num]
    #cluster_num['0']

    frases = []
    for oracion in cluster_num['0']:    #hace una lista con todas las oraciones del cluster
        frases.append(str(oracion).lower())

    diccionario = defaultdict(int) #hace un diccionario de frecuencia con las frases enteras de la lista 'frases'
    for frase in frases:
        diccionario[frase] += 1

    corpus = list(diccionario.keys()) #transforma los keys del diccionario en corpus para volver a correr tf-idf, no uso 'frases' para no tener repeticiones de oraciones

    or_mayor_fq = [] # hago una lista con las oraciones que tenian mayor frecuencia para despues unirlas con los clusters y armar solo esa cantidad de clusters
    for j, i in list(diccionario.items()):
        if i > 1:
            or_mayor_fq.append((j, i)) #adjunto tambien la frecuencia para no perder el 'peso' de cada frase

    if len(or_mayor_fq) == 0:
        return 

    vectorizer = TfidfVectorizer()



    kmeans = KMeans(n_clusters=len(or_mayor_fq)) #hago tantos clusters como oraciones de frecuencia mayor a 1 tengo

    matriz = vectorizer.fit_transform(corpus) 

    kmeans.fit(matriz)

    clusters = [[corpus[i],kmeans.labels_[i]] for i in range(len(corpus))] #tira una lista de listas con frase, cluster

    clusters = pd.DataFrame(clusters) #transforma esa lista en un dataframe
    # clusters = clusters.sort_values(1) #organiza el df por la columna del numero de cluster


    a = cluster_in(or_mayor_fq, clusters, numero) #paso la funcion para los valores de las oraciones con + fq
    print("")
    print("")
    print("")
    print("----------------")
    print("")
    print("")
    print(a)
    print("")
    print("")
    print("")
    print("----------------")
    print("")
    print("")
    # try: 
    #     with open ('jsondata_congrupos/archivo' + str(numero) + '.json', 'w', encoding = 'utf-8') as f:
    #         f.write(json.dumps(a))
    # except:
    #     return


for i in range(150):
    procesar_cluster(int(i))