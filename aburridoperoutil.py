import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import defaultdict
import json


clustercsv = pd.read_csv('clusters150.csv', sep = '*')

for i in range(150):
	cluster_num = clustercsv['1'] == i  #este snippet elige todas las oraciones de un cluster y devuelve la columna '0' como texto 
	cluster_num = clustercsv[cluster_num]
	    #cluster_num['0']

	frases = []
	for oracion in cluster_num['0']:    #hace una lista con todas las oraciones del cluster
	    frases.append(str(oracion).lower())

	diccionario = defaultdict(int) #hace un diccionario de frecuencia con las frases enteras de la lista 'frases'
	for frase in frases:
	   	diccionario[frase] += 1


	or_mayor_fq = [] # hago una lista con las oraciones que tenian mayor frecuencia para despues unirlas con los clusters y armar solo esa cantidad de clusters
	for j, k in list(diccionario.items()):
	    if k > 1:
	        or_mayor_fq.append((j, k))

	if len(or_mayor_fq) == 0 or len(or_mayor_fq) == 1:
		continue

	or_mayor_fq.sort(key=lambda tup: tup[1])
	

	diccionario_pandaFrames = {'name': or_mayor_fq[-1][0], 'size' : or_mayor_fq[-1][1], 'children' : [{'name' : x[0], 'size' : x[1], 'children' : []}  for x in or_mayor_fq[:-1]]} 
	        
	resultado = {
	    	"name":str(i),
	      "size": 500,
	      "children":None
	    }
	resultado['children'] =  [diccionario_pandaFrames]


	with open ('archivosjson/' + str(i) + '.json', 'w', encoding = 'utf-8') as f:
        	f.write(json.dumps(resultado))
    

