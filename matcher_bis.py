##Projet de TC1

from time import time
import os.path
import time
import json
import sys
import os
import re

working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
working_dir += "/Documents/TC1/"
print(working_dir)


##extracteur de villes et CN
def read_City(path):
    """
    extrait les villes et leur countryCode
    output : dictionnaire "ville" -> "CN"
    """
    city_cc = re.compile(r"\'(.*?)\'\|\'([A-Z]{2})\'")
    inp = open(path, 'r')
    in_data = []
    i,l = 0,True
    while l:
        try:
            line = inp.readline()
            if line == '':
                l = False
            m = city_cc.match(line)
            if m is not None:
                in_data.append((m[1], m[2]))
        except:
            print(f'Exception at line {i}')
        i += 1
    print(in_data[:5])
    inp.close()
    f = open(working_dir + 'curated_input.txt', 'w')
    json.dump(in_data, f)
    f.close()
    return in_data

def read_CN(path):
    """
    extrait les CountryCode
    output : dictionnaire "CN" -> "Country Name"
    """
    cn_cc = re.compile(r"([A-Z]{2})\|(.*)")
    name_cc = re.compile(r"\"?([A-Za-z ]+)\|? ?([A-Za-z ]*)\"?")
    inp = open(path, 'r')
    in_data = {}
    i,l = 0,True
    while l:
        try:
            line = inp.readline()
            if line == '':
                l = False
            m = cn_cc.match(line)
            if m is not None:
                name = name_cc.match(m[2])
                if name[2] != '':
                    name = name[2] + " " + name[1]
                else:
                    name = name[1]
                in_data[m[1]] = name
        except:
            print(f'Exception at line {i}')
        i += 1
    inp.close()
    f = open(working_dir + 'curated_CN.txt', 'w')
    json.dump(in_data, f)
    f.close()
    return in_data

##Agrégateur de doublons
def unique_city_name(l):
    """
    agrège les villes en double ensemble en comptant le nombre d'occurance de chaque couple "ville"-"CN"
    l : list[("ville","CN")]
    output : renvoie un dictionnaire "ville" -> dict{"CN":int}
    """
    dic = {}
    i,j = 0,1
    for e in l:
        if e[i] in dic:
            if e[j] in dic[e[i]]:
                dic[e[i]][e[j]] += 1
            else:
                dic[e[i]][e[j]] = 1
        else:
            dic[e[i]] = {e[j] : 1}
    f = open(working_dir + 'unique_city.txt', 'w')
    json.dump(dic, f)
    f.close()
    return dic 

##Compacteur : renvoie l'output demandé
def makeOutput(inputCity,uniqueCity,sortCity,realName,mapCity,labelClean,country,file,returned=True):
    """
    créer le fichier [file].txt contenant les lignes en uppercase :
    
            "InputCity|CN|OutputCity|CountryName|REMARK"
    
    pour chaque item de [inputCity]
    INPUT:
        inputCity : list[("ville","CN"]
        uniqueCity : dictionnaire "ville" -> dict{"CN":_}
        sortCity : dictionnaire "ville" -> "ville_clean_sorted"
        realName : dictionnaire "ville_clean_sorted" -> "real_ville_clean_sorted" 
                  ("real_ville_clean_sorted" est équivalent à "ville_clean_sorted")
        mapCity : dictionnaire "ville_clean_sorted" -> "ville_clean"
        labelClean : dictionnaire "ville_clean_sorted" -> dict{"CN":_}
        country : dictionnaire "CN" -> "CountryName"
        file : nom du fichier de sortie (sans extension)
    OPTIONS:
        returned (True/False) : True si la liste des lignes doit être renvoyée en fin de programme
    OUTPUT:
        list[InputCity,CN,OutputCity,CountryName]
    """
    f = open(working_dir + file + ".txt","w")
    listToWrite = []
    for city,cn in inputCity:
        inc = False
        if(city in uniqueCity): #toutes les villes sont dans uniqueCity sauf les null
            #Récupération du nom réel de la ville
            sortedCity = None
            if(city not in sortCity or sortCity[city] not in realName):
                cityName = city
                inc = True
            else:
                sortedCity = realName[sortCity[city]]
                cityName = mapCity[sortedCity]
            #récupération du nom réel du pays
            if(cn not in country):
                #tentative de rattrapage du label faux grâce au label prédominant de la classe de nom
                listCN = list(labelClean[sortedCity].keys())
                listInt = list(labelClean[sortedCity].values())
                i = np.argmax(listInt)
                if(listCN[i] not in country):
                    countryName = "FALSE DATA" #certain label associé n'existe pas dans le map des CN, ils sont donc faux
                    inc = True
                else:
                    countryName = country[listCN[i]] #rattrapage du label faux grâce au label prédominant de la classe de nom
            else:
                countryName = country[cn]
            listLign = [city,cn,cityName,countryName]
            if(inc):
                listLign.append("INCOHERENT DATA") #data incohérente (mauvais label, numéro de téléphone, nom clairement faux et ne correspondant à aucune autre ville, etc...)
        else:
            listLign = [city,cn,city,cn,"NULL DATA"] #donnée null de la forme ('','CN')
        #écriture dans le fichier de sortie
        f.write(("|".join(listLign)+"\n").upper())#.capitalize())
        if(returned):
            listToWrite.append(listLign)
    f.close()
    if(returned):
        return listToWrite
    else:
        return None

##écriture de la liste des villes
def write_city_name(dic):
    f = open(working_dir + "city_name.txt","w")
    sorted_cities = list(dic.keys())
    sorted_cities.sort()
    print(sorted_cities[:10])
    for elt in sorted_cities:
        f.write(f"{elt}\n")
    f.close()