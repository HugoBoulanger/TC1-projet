##Projet TC1 - clustering

from time import time
import numpy as np
import sklearn.cluster
import random
import os.path
import copy
import json
import sys
import os
import re

def unique_city(l):
    """
    agrège les villes en double ensemble en comptant le nombre d'occurance de chaque couple "ville"-"CN"
    l : list[("ville","CN")]
    output : renvoie une liste [("ville","CN","occ")]
    """
    dic = {}
    liste = []
    i,j = 0,1
    for e in l:
        if e[0]+"#|#"+e[1] in dic:
            dic[e[0]+"#|#"+e[1]] += 1
        else:
            dic[e[0]+"#|#"+e[1]] = 1
    for key,elt in dic.items():
        key1,key2 = key.split("#|#")
        liste.append((key1,key2,elt))
    return liste 

##implémentation du K-means
def k_means(K,X,distance,maxIter = None):
    """
    calcule K clusters avec K-means et une distance custom
    INPUT:
        K : nombre de clusters
        data : données à clusturiser
        distance : fonction de distance - data -> float
    OUTPUT:
        clusters : dict{int : (éléments du cluster, centroïde du cluster)}
        error : score final d'erreur de classification
    """
    print(f"début K-means :\n{K} clusters\n{maxIter} itérations")
    # To store the value of centroids when it updates
    X.sort(key=lambda tup : tup[2]) #trie par occurence (on va considérer que les 11000 villes les plus représenter sont les bonnes -> euristique nulle)
    centroids = [X[i] for i in range(K)] #initialisation des centroïds
    random.shuffle(X)
    # Cluster Labels(0, 1, 2)
    clusters = np.zeros(len(X))
    #elements of cluster
    elements = dict([(i,[]) for i in clusters])
    print(f"centroïds : {centroids[:2]}\nclusters : {clusters[:2]}\nelements : {list(elements.items())[:2]}")
    # Error func. - Distance between new centroids and old centroids
    error = 1 #dist(C, C_old, None)
    iter = 0
    print(f"chaque itération prendra {2*(len(X)/200)} lignes environ")
    # Loop will run till the error becomes zero
    while (maxIter != None and iter > maxIter) or (error != 0): #while en maxIter*K*len(X)
        #elements of cluster
        elements = dict([(i,[]) for i in clusters])
        # Assigning each value to its closest cluster
        for i in range(len(X)): #boucle K*len(X)
            distances = [distance(X[i], centroids[j]) for j in range(K)]
            cluster = np.argmin(distances)
            clusters[i] = cluster
            print(".",end="")
        # Storing the old centroid values
        print("")
        centroids_old = copy.deepcopy(centroids)
        # Finding the new centroids by taking the average value
        for i in range(K): #boucle en K*len(X)
            points = [X[j] for j in range(len(X)) if clusters[j] == i]
            centroïds[i] = points[np.argmin(points - np.mean(points, axis=0))]
            print(".",end="")
        # Compute new error
        error = np.linalg.norm(centroids - centroids_old)
        iter+=1
        print(f"\nend of iteration {iter}")
    C = dict([(key,(elt,centroïds[key])) for key,elt in elements.items()])
    return C,error

def distanceCity(c1,c2):
    """
    INPUT :
        c1, c2 : tuple ("nom de ville","CN")
    OUTPUT :
        dist : float
    """
    d1 = compareString(c1[0],c2[0]) #distance de Levenshtein
    d2 = distanceCN(c1[1],c2[1])
    return d1 + d2
    
def distanceCity2(c1,c2):
    """
    INPUT :
        c1, c2 : triplet ("nom de ville","CN","occurence")
    OUTPUT :
        dist : float
    """
    d1 = compareString(c1[0],c2[0]) #distance de Levenshtein
    d2 = distanceCN(c1[1],c2[1])
    d3 = min(c1[2],c2[2])/max(c1[2],c2[2]) #impact de l'occurrence
    return d1 + d2 + d3

def distanceCN(cn1, cn2):
    """
    GLOBALS :
        CN : enumérable (list, dic, etc) contenant la liste réelle des CN autorisés
    INPUT :
        cn1, cn2 : chaîne CN (chaîne de 2 carac uppercase)
    OUTPUT : 
        dist : float
    """
    if(cn1 not in CN or cn2 not in CN):
        return 0 #on considère que les CN sont identiques et que leur différence est une erreur de saisie
    elif(cn1 != cn2):
        return 1
    else:
        return 0
        
##Exécution
top = time()
print("DEBUT DU CALCUL")
#in_data = read_City(working_dir + 'Problem 3 Input Data.txt')
#random.shuffle(in_data)
scoreSim = 0.72 #limite de similarité utilisé
labelLim = 2
labelSeuil = 1000
unique_city_occ = unique_city(in_data)
print(f"data extraits en {round(time()-top)}s\ntaille données initiales : {len(in_data)}\ntaille des données sans doublons : {len(unique_city_occ)}")
CN = read_CN(working_dir + 'Problem 3 Input Data - Country Map.txt')
random.shuffle(unique_city_occ)
#learning
# Y,error = k_means(11000,in_data[:500000],distanceCity,maxIter=1) #TROP LONG
Y,error = k_means(11000,unique_city_occ,distanceCity2,maxIter=1)
print(f"erreur K-means : {error}")
print(f"FIN D'EXECUTION : {round(time()-top)}s")