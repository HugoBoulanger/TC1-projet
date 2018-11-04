##Projet TC1 - Main

from time import time
import numpy as np
import os.path
import json
import sys
import os
import re

working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
working_dir += "/Documents/TC1/" #répertoire à changer
print(working_dir)

#0) extraire les données du fichier initial
#1) agréger les doublons
#2) supprimer les nulls
#3) supprimer les incohérents faciles
#4) supprimer les termes inutiles                           -> on sauve quelque part l'association "terme initial" -> "terme nettoyé"
#5) replacer les sous-mots par ordre alphabétique (trie)    -> on sauve quelque part l'association "terme initial" -> "terme inversé"
#6) agréger les similaires
#7) retirer les incohérents difficiles (classe 1 représentant, caractères incohérents dans le représentant, peu de représentativité)
#8) choisir le représentants de chaque classes de similaires
#8.5) corriger les erreurs d'agrégation facilement rattrapables
#9) corriger les countryCode faux (peu représenté) : remplacement par le plus prépondérent
#10) extraire correctement les noms de country
#11) écrire le fichier de sortie : InputCity, CN, OutputCity, CountryName
#       --> demande de remonter la chaîne de dictionnaires générée


#0)
in_data = read_City(working_dir + 'Problem 3 Input Data.txt') 
scoreSim = 0.72 #limite de similarité utilisé
#for testing
in_data_test = []
testLimit = 20000
iter = 0
for elt in in_data:
    if(iter == 2*testLimit):
        break
    if(iter%2==0):
        in_data_test.append(elt)
    iter+=1
#in_data = in_data_test #comment to desactivate testing
#1)
print(f"taille données : {len(in_data)}\ntaille données de test de script : {len(in_data_test)}")
unique_city = unique_city_name(in_data) #dict : "ville" -> dic{"CN" : int}
write_city_name(unique_city)
#2)
print(f"nombre de villes uniques avant suppression des nulls : {len(unique_city)}")
del unique_city['']
print(f"nombre de villes uniques après suppression des nulls : {len(unique_city)}")
#3) & 4)
clean_city1 = cleanData(unique_city.keys()) #dict : "ville" -> "ville_clean"
#5)
clean_city = sortData(clean_city1) #dict : "ville" -> "ville_sort"
clean_city2 = {}
for key,elt in clean_city.items():
    clean_city2[elt] = clean_city1[key] #dict : "ville_sorted" -> "ville_clean"
#6)
print(f"taille du dictionnaire nettoyé : {len(clean_city.keys())}\nDébut agrégation : ",end ="")
clean_city_sort = list(clean_city.values())
clean_city_sort.sort()
agregate_city1 = aggregate(clean_city_sort,scoreSim,"similarity")
print(f"nombre de classes de villes équivalentes : {len(agregate_city1)}")
#7)
agregate_city2 = deleteIncoherents(agregate_city1)
print(f"nombre de classes de villes équivalentes après suppression des incohérents : {len(agregate_city2)}")
#8)
labelClean = {}
for key,elt in unique_city.items():
    if key in clean_city.keys():
        labelClean[clean_city[key]] = elt #dict : "ville_sort" -> dic{"CN" : int}
agregate_city = trueRepresentant(agregate_city2,labelClean,"correspondance")
#9)
#TODO
#10)
CN = read_CN(working_dir + 'Problem 3 Input Data - Country Map.txt')
#11)
finalOutput = makeOutput(in_data,unique_city,clean_city,agregate_city,clean_city2,labelClean,CN,"output")