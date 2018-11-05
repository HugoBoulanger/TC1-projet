##Correction orthographique

from time import time
import numpy as np
import json
import re


##Test de Similarité
def compareString(str1,ref):
    """
    str1 : chaine de caractère à comparer
    ref : chaine de caractère de référence
    retourne le score de similarité de str1 par rapport à ref
    """
    longer = str1
    shorter = ref
    if(len(longer) < len(shorter)):
        longer,shorter = shorter,longer
    if(len(longer) == 0):
        return 1.0
    else:
        return (len(longer) - editDistance(longer.lower(),shorter.lower())) / len(longer)
        
def editDistance(str1,str2):
    """
    calcule la distance entre str1 et str2
    str1 est une chaine plus longue que str2
    """
    #print(len(str1),len(str2))
    cost = [0 for i in range(len(str1)+1)]
    for i in range(len(str1)+1):
        lastValue = i
        for j in range(len(str2)+1):
            if(i == 0):
                cost[j] = j
            else:
                if(j > 0):
                    newValue = cost[j-1]
                    if(str1[i-1] != str2[j-1]):
                        newValue = min(min(newValue,lastValue),cost[j]) + 1
                    cost[j-1] = lastValue
                    lastValue = newValue
        if(i > 0):
            cost[len(str2)] = lastValue
    return cost[len(str2)]

def aggregate(data,limite,file):
    """
    data : ensemble itérable de chaînes de caractères dont certaines sont proches
    limite : flottant entre 0. et 1. : rapport de ressemblance autorisé entre 2 chaînes pour les considérer comme égales
    file : nom du fichier où sauver le retour (sans extension)
    """
    top = time()
    dic = {}
    iter = 0
    print(f"{len(data)} data")
    print(f"fin dans environ {len(data)/200} lignes")
    print(200*".") #affiche 200 . (environ 1 ligne de console), pour visualiser plus précisément la progression
    for elt in data:
        #print(elt)
        score = 0
        value = ""
        for exp in dic.keys():
            #print(f"{elt} vs {exp}")
            newScore = max(score,compareString(exp,elt))
            if newScore != score:
                value = exp
            score = newScore
        if(score > limite): #limite de ressemblance entre deux mots, plus la limite est haute, plus la comparaison sera stricte
            dic[value].append(elt)
        else:
            dic[elt] = []
        iter += 1
        if(iter%200 == 0):
            print(f"\nligne {iter/200}, dic a {len(dic.keys())} clés")
        print(".",end="")
    print(f"\ntemps de calcul : {int(time()-top)}s\nnouveau nombre de clés : {len(dic)}\nsauvegarde du fichier...",end="")
    f = open(working_dir + file + ".txt","w")
    for elt in dic.keys():
        toPrint = "> "+elt+"\n"
        f.write(toPrint)
        for valueDic in dic[elt]:
            toPrint = "----- "+valueDic+"\n"
            f.write(toPrint)
        f.write("##############\n")
    f.close()
    f = open(working_dir + file + "DUMP.txt","w")
    json.dump(dic,f)
    f.close()
    print(" ... achevée")
    print(f"durée totale : {int(time() - top)}s")
    return dic
    
##Nettoyage et Traitement de l'agrégation
def trueRepresentant(dic,dataLabel,file):
    """
    prend le résultat de "aggregate" et transforme les clés pour obtenir le véritable représentant (celui qui a la bonne orthographe)
    newDic : dictionnaire des villes similaires (résultat de "aggregate")
    dataLabel : dictionnaire {"ville" : [liste de CN]}
    file : nom du fichier où sauver le retour (sans extension)
    """
    newDic = {} #forme {"ville" : "ville"}
    for elt in dic.keys():
        listName = [elt]+dic[elt]
        referance = []
        label = []
        for city in listName:
            firstLabel = list(dataLabel[city].keys())[0]
            label.append(firstLabel)
            referance.append(dataLabel[city][firstLabel]) #normalement de type int
        i = np.argmax(referance)
        labelI = label[i]
        for city in listName:
            j = np.argmax(list(dataLabel[city].values()))
            labelJ = list(dataLabel[city].keys())[j]
            if(labelI == labelJ):
                newDic[city] = listName[i]
            else:
                newDic[city] = city #pas le même pays prédominant, c'est sans doute une erreur d'agrégation
    print(f"taille de newDic = {len(newDic)}/{len(dataLabel)}") #doit être égal au nombre de ville
    f = open(working_dir + file + ".txt","w")
    for elt in newDic.keys():
        toPrint = elt + " : " + newDic[elt] + "\n"
        f.write(toPrint)
    f.close()
    f = open(working_dir + file + "DUMP.txt","w")
    json.dump(newDic,f)
    f.close()
    return newDic
    
def deleteIncoherents(data):
    """
    data : dictionnaire "ville" -> "[liste villes]"
    supprime les clés comportant des caractères incohérents (chiffres, ponctuations, etc...) qui n'ont qu'un seul représentant
    """
    dic = {}
    incoherent = re.compile(r".*[^A-Za-z., \-\"\'\\\/]+.*")
    for key,elt in data.items():
        if (incoherent.match(key) and len(elt) == 0):
            pass
        else:
            dic[key] = elt
    return dic

##Nettoyage des données brutes
def cleanData(data):
    """
    data : énumérable de villes
    nettoyage :
        - supprime les termes : AVENUE, STREET, CITY, CIUDAD, CEDEX, () en fin de chaîne.
        - élimine du set initial tous les éléments ne comportant pas de termes alphabétiques (ex : numéros de téléphone)
    """
    avenue = re.compile(r".* *AVENUE")
    street = re.compile(r".* *STREET")
    city = re.compile(r".*-? ?CITY")
    ciudad = re.compile(r".* ?-?CIUDAD")
    town = re.compile(r".* ?-?TOWN")
    cedex = re.compile(r".* *CEDEX.*")
    nombre = re.compile(r"[^A-Za-z]+")
    nombreFin = re.compile(r".+ ?[^A-Za-z]+")
    parenthese = re.compile(r".+\(.+\)")
    dic = {}
    for elt in data:
        if nombre.match(elt) is not None:
            pass #on ne les veut pas dans le set final
        elif avenue.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ]) *AVENUE",r"\g<before>",elt)
        elif street.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ]) *STREET",r"\g<before>",elt)
        elif city.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ])-? ?CITY(?P<after>[A-Z ])",r"\g<before>\g<after>",elt)
        elif ciudad.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ])-? ?CIUDAD(?P<after>[A-Z ])",r"\g<before>\g<after>",elt)
        elif town.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ])-? ?TOWN(?P<after>[A-Z ])",r"\g<before>\g<after>",elt)
        elif parenthese.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ]) *\(.+\)",r"\g<before>",elt)
        elif cedex.match(elt) is not None:
            dic[elt] = re.sub(r"(?P<before>.+[^ ]) *CEDEX.*",r"\g<before>",elt)
        elif nombreFin.match(elt):
            dic[elt] = re.sub(r"(?P<before>.+[^ ]) *[^A-Za-z]+$",r"\g<before>",elt)
        else:
            dic[elt] = elt
    return dic
    
def sortData(data):
    """
    data : dictionnaire "ville" -> "ville"
    nettoyage :
        - réorganise les chaînes de plusieurs mots en triant les sous-mots par ordre alphabétique
    """
    dic = {}
    for key,elt in data.items():
        listMot = elt.split(" ") #on récupère les sous-mots
        listMot.sort()
        eltFinal = " ".join(listMot) #chaîne avec les sous-mots triés
        dic[key] = eltFinal
    return dic
    
def suppLabel(data,a,seuil):
    """
    supprime les labels probablement faux des données
    data : dictionnaire : "ville" -> dict{"CN":int}
    a : nombre de labels au dessus duquel des coupes sont envisagées (int min 1)
    seuil : int > 1
    output : dictionnaire : "ville" -> dict{"CN":int}
    """
    dic = {}
    nb = {}
    j = 0 #for function' stat
    k = 0 #for function' stat
    m = 0 #for function' stat
    n = 0 #for function' stat
    o = 0 #for function' stat
    b = a+2 #nombre de labels à partir duquel on considère qu'il y en peu (for function' stat)
    c = a+4 #nombre de labels à partir duquel on considère qu'il y en a bcp (for function' stat)
    for key,elt in data.items():
        if(len(elt) > a):
            supp = False
            m+=1
            if(len(elt) in nb):
                nb[len(elt)] += 1
            else:
                nb[len(elt)] = 1
            if(len(elt) < b):
                n+=1 #ville avec moins de 4 labels (labels probablement bons
            elif(len(elt) > c):
                o+=1 #ville avec plus de 7 labels (labels probablement faux)
            i = np.max(list(elt.values()))
            eltcopy = elt.copy()
            for cn in elt:
                if elt[cn] < round(i/seuil):
                    j+=1
                    supp = True
                    del eltcopy[cn]
            if(supp):
                k+=1 #ville a subis des coupes dans ses labels
            dic[key] = eltcopy
        else:
            dic[key] = elt
    print(f"{m} villes avec plus de {a} labels dont\n{n} avec {b-1} labels et\n{o} avec plus de {c} labels\n{k} villes avec labels supprimés\n{j} labels supprimés") #function' stat
    print(nb)
    return dic

##Test sur des sous-ensembles de city_name.txt
# listcities = list(unique_city.keys())
# listcities.sort()
# testDic75 = aggregate(listcities,0.75,"similarity75") #COMPUTE ON ALL CITIES
# testDic65 = aggregate(listcities,0.65,"similarity65") #COMPUTE ON ALL CITIES
# testDic7 = aggregate(list(listcities,0.7,"similarity7") #COMPUTE ON ALL CITIES
# testDic5 = aggregate(list(listcities,0.5,"similarity5") #COMPUTE ON ALL CITIES

adelaide = ['ADELAAIDE','ADELADE','ADELAID','ADELAIDE - SA','ADELAIDE SA','ADELAIDE','ADELAIDE, SA','ADELAIDE,','ADELAIDEE','ADELAIDEPARK','ADELAIDEV','ADELANTO','ADELIADE S.A.','ADELIADE','ADELIDE'] #test classique : 1 classe attendue
aguacaliente = ['AGUACALIENTES','AGUAS CALIENTES','AGUASCAILIENTES','AGUASCALEINETES','AGUASCALEINTES','AGUASCALENTES','AGUASCALIENES','AGUASCALIENTE','AGUASCALIENTES','AGUASCALIENTES, A','AGUASCALIENTES,','AGUASCALIENTES,AG','AGUASCALIENTESS','AGUASCALIENTS','AGUASCAUENTES','AGUSACALIENTES','AGUSCALIENTES'] #test facile : 1 classe attendue
huntingwood = ['HUNTIGDON','HUNTIGNWOOD','HUNTIGWOOD','HUNTIMDON','HUNTINDON','HUNTINGDOM VALLY','HUNTINGDOM-EX','HUNTINGDOM-EX-','HUNTINGDON VALLEY','HUNTINGDON VALLY','HUNTINGDON','HUNTINGDON-EX','HUNTINGDON-EX-','HUNTINGOOD','HUNTINGSON VALLEY','HUNTINGTON BCH','HUNTINGTON BEACH','HUNTINGTON PARK','HUNTINGTON STATIN','HUNTINGTON STATIO','HUNTINGTON VALLEY','HUNTINGTON VALLY','HUNTINGTON','HUNTINGWOOD NSW','HUNTINGWOOD','HUNTINGWOODD','HUNTINGWOODS','HUNTINGWOOOD','HUNTINGWWOD','HUNTINWOOD'] #1 classe attendue
levallois = ['LEVAL  TRAHEGNIES','LEVAL TRAHEGNIES','LEVALLIIS-PERRET','LEVALLIOS PERRET','LEVALLIOS','LEVALLIS PERRET','LEVALLIS-PERET','LEVALLIS-PERRET X','LEVALLIS-PERRET','LEVALLIS0PERRET','LEVALLLOIS-PERRET','LEVALLOIF-PERRET','LEVALLOIS - PERRT','LEVALLOIS -PERRET','LEVALLOIS PERET','LEVALLOIS PERRET','LEVALLOIS PERRETT','LEVALLOIS"PERRET','LEVALLOIS','LEVALLOIS-PERET','LEVALLOIS-PERRET','LEVALLOIS-PERRET1','LEVALLOIS-PERRETT','LEVALLOISPERRET','LEVALLOS-PERRET','LEVALLOUIS-PERRET','LEVALOIS PERRET','LEVALOIS-PERRET','LEVANGER'] #test moyen, 3 classes attendues
nizny = ['NIZHINIY NOVOGRAD','NIZHINY NOVGOROD','NIZHNI NOVGOROD','NIZHNIJ NOVGOROD','NIZHNIY NORFOROD','NIZHNIY NOVGOROD','NIZHNIY NOVOGORD','NIZHNIY NOVOGOROD','NIZHNIY NOVOGRAD','NIZHNIY NOVOGROD','NIZHNY NOVGOROD','NIZHNYI NOVGOROD','NIZHNYI NOVGORORD','NIZNIY','NIZNY NOVGOROD','NIZNY NOVGORODOD'] #test moyen : 1 classe attendue
saint = ['SAIN MICHEL','SAINT  NAZAIRE','SAINT ALBAN','SAINT AUBIN','SAINT BEAUZIRE','SAINT BENOIT CEDE','SAINT BENOIT CEDX','SAINT BENOIT','SAINT BERTHEVIN','SAINT BETERSBURG','SAINT BRIEUC','SAINT CERE','SAINT CLOUD','SAINT COULOMB','SAINT CYR SUR LOI','SAINT CYR','SAINT DENIS DE L','SAINT DENIS DE LN','SAINT DENIS','SAINT DENNIS','SAINT DIE DES V.','SAINT DIE DES VO.','SAINT ETIENNE CED','SAINT ETIENNE','SAINT FELIU','SAINT GALLEN','SAINT GELY D.FESC','SAINT GELY DU F.','SAINT GELY DU FE.','SAINT GELY DU FEC','SAINT GELY DU FES','SAINT GELY DU','SAINT GELY DUFESC','SAINT GELY FESC','SAINT GELY','SAINT GERMAIN DU','SAINT GERMAIN S/','SAINT GERMAIN','SAINT GIRONS','SAINT GREGOIRE','SAINT HERBLAIN','SAINT ISMIER','SAINT JACQUES','SAINT JEAN DE VES','SAINT JOHN','SAINT JOSEPH','SAINT JOSPEH MI','SAINT LAURENT DU','SAINT LAURENT M.','SAINT LAURENT NOU','SAINT LAURENT','SAINT LEONARDS','SAINT LEU D"ESSER','SAINT LO','SAINT LOUIS PARK','SAINT LOUIS','SAINT LOUIS, MO','SAINT MANDE','SAINT MARTIAL DE','SAINT MARTIAL VIE','SAINT MARTIAL VIT','SAINT MARTIN','SAINT MAX','SAINT MICHEL DE','SAINT MICHEL','SAINT NAZAIRE','SAINT NICOLAS','SAINT NIKLAAS','SAINT NIKLAUS','SAINT ORENS DE G.','SAINT OUEN AUMONE','SAINT OUEN L"AUMO','SAINT OUEN','SAINT PATERSBURG','SAINT PAUL','SAINT PERERSBURG','SAINT PERETSBURG','SAINT PETERBURG','SAINT PETERSBOURG','SAINT PETERSBRUG','SAINT PETERSBURG','SAINT PETESBURG','SAINT PIERRE D OE','SAINT PIERRE D"OL','SAINT PIERRE DE N','SAINT PIERRE MONT','SAINT PIERRE','SAINT PRIECT','SAINT PRIEST EN J','SAINT PRIEST EN Z','SAINT PRIEST EN','SAINT PRIEST','SAINT QUENTIN','SAINT QUINTEN','SAINT REMY LE VAN'] #test difficile, bcp de villes sont différentes (pas compté le nombre de classes attendues)
san = ['SAN FERNANDO','SAN FRACISCO','SAN FRAN DOS RIOS','SAN FRAN','SAN FRANCISC0','SAN FRANCISCO 492','SAN FRANCISCO','SAN FRANCISCO, CA','SAN FRANCISCOO','SAN FRANCISO','SAN FRANCSICO','SAN FRANSCISCO','SAN FRANSICO','SAN FRANSISCO','SAN GERMAN','SAN GIOVANNI ROT)','SAN GIOVANNI ROT.','SAN GIOVANNI ROTO','SAN GIOVANNI','SAN ISIDRO CUATIT','SAN ISIDRO LIMA','SAN ISIDRO','SAN ISIDRO, BUENO','SAN ISIDRO, BUNOS','SAN ISIDRO, LIMA','SAN ISIDRO,LIMA','SAN ISIDRO-LIMA','SAN ISIDRO; LIMA','SAN ISISDRO','SAN ISISDRO, BUEO','SAN JAUN','SAN JERONIMO TEPE','SAN JERONIMO','SAN JOAQUIN','SAN JOSE DOS CAMP','SAN JOSE','SAN JOSE, CARACAS','SAN JOSE,','SAN JUAN CAPISTRA','SAN JUAN CAPISTRO','SAN JUAN CITY','SAN JUAN DE ALICE','SAN JUAN DE LURIG','SAN JUAN M.D.','SAN JUAN','SAN JUAN-ALICANTE',
'SAN JUSTO','SAN JUSTO, BUENOS','SAN KUIS POTOSI','SAN LAZZARO DI','SAN LEANDRO','SAN LEANDRO, CA','SAN LUCAR DE BARA','SAN LUIIS POTOSI','SAN LUIS DE POT','SAN LUIS DE POTO','SAN LUIS DE POTOI','SAN LUIS DE POTOS','SAN LUIS OBISPO','SAN LUIS POTOS','SAN LUIS POTOSI','SAN LUIS POTOSI,','SAN LUIS PTOSI','SAN LUIS','SAN LUIS, SAN LUI','SAN LUIZ POTOSI','SAN LUIZ','SAN LYUIS POTOSI','SAN MARCO IN LAMS','SAN MARCOS','SAN MARINO DI LUP','SAN MARTIN B.A.','SAN MARTIN DE POR','SAN MARTIN DE POS','SAN MARTIN PORRES','SAN MARTIN','SAN MARTIN, BUENO','SAN MARTIN,B.A.','SAN MARTINO','SAN MATEO','SAN MIGUEL DE T','SAN MIGUEL DE T.','SAN MIGUEL DE TU','SAN MIGUEL DE TU.','SAN MIGUEL DE TUC','SAN MIGUEL DE TUN','SAN MIGUEL','SAN MIGUEL, BUENO','SAN MIGUEL, SANTI','SAN MIGUELTUCUMAN','SAN MINIATO','SAN NICOLAS DE LO','SAN NICOLAS','SAN NICOLAS, BUEN','SAN PABLO','SAN PAOLO','SAN PAULO','SAN PEDRO DE SULA','SAN PEDRO GARZA','SAN PEDRO SULA','SAN PEDRO SULA,','SAN PEDRO ZULA','SAN PEDRO','SAN PEDRO, BUENOS','SAN RAFAEL','SAN RAFAEL, MENDO','SAN RAFAL','SAN RAMON','SAN SABASTIAN','SAN SALVADOR','SAN SEBASTIAN DES','SAN SEBASTIAN','SANAA','SANATA FE','SANATIAGO','SAND DIEGO','SAND','SANDANDER','SANDEFJORD','SANDHURST','SANDIEGO','SANDNES','SANDOMIERZ','SANDRINGHAM','SANDRINHAM','SANDTON CITY','SANDTON GAUTENG','SANDTON','SANDUSKY','SANDVIKA','SANDWHICH','SANDWICH','SANDWICH, KENT','SANDY','SANF FRANCISCO','SANFRANCISCO','SANG-MI LEE','SANGERHAUSEN','SANGTA FE','SANGTIAGO'] #test difficile, bcp de villes sont différentes (pas compté le nombre de classes attendues)
york = ['EW YORK','NEW TORK','NEW-YORK','NEW Y0RK','NEW YOEK','NEW YOR','NEW YORK 10013','NEW YORK CITY','NEW YORK','NEW YORK, NY','NEW YORK,','NEW YORK-MANHATTN','NEW YOTK','NEW YOUR','NEW YROK','YORK'] #test difficile, 2 classes attendues (York et New York)
withF = ['FLORO','FLORSHEIM','FLOWOOD','FLUGHAFEN ZURICH','FLUGHAFEN','FLUSHING','FOCA','FOCH','FOCSANI','FOEHREN','FOGGIA','FOGGIA.','FOIANO DI VAL FO.','FOIX','FOLIGNIO','FOLIGNO','FOLIGNO/VITERBO','FOLLEBU','FOLLINSDORF','FOMEL KHALIG','FONDETTE','FONDETTES','FONTAINE','FONTAINEBLEAU','FONTAN','FONTANAFEDDA','FONTANAFREDDA','FONTE NUOVA','FONTENAY AUX ROSE','FONTENAY LE COMTE','FONTENAY SOUSBOIS','FONTENAY TRESIGNY','FONTENAY-AUX-ROSE','FONTENAY-AUX-ROSS','FONTENILLE','FONTENILLES','FONTENNILLE','FOOOTSCRAY','FOOTSCARY','FOOTSCRAY','FOOTSCRAY, VIC','FOOTSCRAY,VIC','FOR COLLINS','FORALAEZA','FORALEZA''FORATALEZA,CEARA','FORCALQUIER','FORCHHEIM','FORDHAM CAMBS','FORDHAM','FORDINGBRIDGE','FORDSBURG','FOREST ROW','FOREST VIA NYC','FOREST','FORHAM','FORLI','FORMOSA','FORMOSA, FORMOSA','FORSTER CITY','FORT COLLINS']
total = adelaide+aguacaliente+withF+huntingwood+nizny+saint+san+york #tous les exemples précédents