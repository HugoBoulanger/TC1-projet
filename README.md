# TC1-projet

Démarche :
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