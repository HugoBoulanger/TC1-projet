# TC1-projet

D�marche :
#0) extraire les donn�es du fichier initial
#1) agr�ger les doublons
#2) supprimer les nulls
#3) supprimer les incoh�rents faciles
#4) supprimer les termes inutiles                           -> on sauve quelque part l'association "terme initial" -> "terme nettoy�"
#5) replacer les sous-mots par ordre alphab�tique (trie)    -> on sauve quelque part l'association "terme initial" -> "terme invers�"
#6) agr�ger les similaires
#7) retirer les incoh�rents difficiles (classe 1 repr�sentant, caract�res incoh�rents dans le repr�sentant, peu de repr�sentativit�)
#8) choisir le repr�sentants de chaque classes de similaires
#8.5) corriger les erreurs d'agr�gation facilement rattrapables
#9) corriger les countryCode faux (peu repr�sent�) : remplacement par le plus pr�pond�rent
#10) extraire correctement les noms de country
#11) �crire le fichier de sortie : InputCity, CN, OutputCity, CountryName
#       --> demande de remonter la cha�ne de dictionnaires g�n�r�e