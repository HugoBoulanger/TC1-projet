##Projet TC1 - Main

from os import system, listdir, getcwd, chdir, mkdir, access, F_OK
from os.path import isfile, join, basename
from subprocess import check_call, DEVNULL
from time import time
import numpy as np
import os.path
import json
import sys
import os
import re

working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
working_dir += "/Documents/TC1/"
print(working_dir)

#1) agréger les doublons
#2) supprimer les nulls
#3) supprimer les incohérents faciles
#4) supprimer les termes inutiles                           -> on sauve quelque part l'association "terme initial" -> "terme nettoyé"
#5) replacer les sous-mots par ordre alphabétique (trie)    -> on sauve quelque part l'association "terme initial" -> "terme inversé"
#6) agréger les similaires
#7) choisir le représentants de chaque classes de similaires
#8) retirer les incohérents difficiles (classe 1 représentant, caractères incohérents dans le représentant, peu de représentativité)
#9) corriger les countryCode faux (peu représenté) : remplacement par le plus prépondérent
#10) écrire le fichier de sortie : InputCity, CN, OutputCity, CountryName

