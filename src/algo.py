# function qui prend en argument la liste des épisodes et qui return les infos épisodes par chaine, pays et les mots récurrents par titre de serie


def infos_episode(liste_episodes):
    # création dictionnaire pour y inserer les infos
    resultat =  {
                "episodes_par_chaine":{},
                "episodes_par_pays":{},
                "mots_recurrents":{}
                
            }
    # liste de chaque titre sans doublon
    liste_titres=[]

    # liste des mots dans les titres
    liste_mots=[]

    # boucle sur chaque episode
    for episode in liste_episodes:
        # si la chaine n'a pas encore été référencé on initialise la valeur à 1 sinon on incrémente de 1
        if episode["chaine"] not in resultat["episodes_par_chaine"]:
            resultat["episodes_par_chaine"][episode["chaine"]]=1
        else:
            resultat["episodes_par_chaine"][episode["chaine"]] += 1

        # si le pays n'a pas encore été référencé on initialise la valeur à 1 sinon on incrémente de 1
        if episode["origine"] not in resultat["episodes_par_pays"]:
            resultat["episodes_par_pays"][episode["origine"]]=1
        else:
            resultat["episodes_par_pays"][episode["origine"]] += 1

        # si le titre n'a pas encore été référencé on l'ajoute à la liste
        if episode["nom série"] not in liste_titres:
            liste_titres.append(episode["nom série"])
    
    # boucle sur tout les titres
    for titre in liste_titres:

        # boucle sur chaque mot de chque titre pour inserer le mot dans la liste "liste_mots" et mettre à jour dans le dictionnaire la récurrence du mot dans la liste "liste_mots"
        for mot in titre.split(" "):
            liste_mots.append(mot)
            resultat["mots_recurrents"][mot]=liste_mots.count(mot)

    # tri chaque dictionnaire dans l'ordre décroissant 
    resultat["episodes_par_chaine"] =dict(sorted(resultat["episodes_par_chaine"].items(), key=lambda item: item[1], reverse=True))
    resultat["episodes_par_pays"] =dict(sorted(resultat["episodes_par_pays"].items(), key=lambda item: item[1], reverse=True))
    resultat["mots_recurrents"] =dict(sorted(resultat["mots_recurrents"].items(), key=lambda item: item[1], reverse=True))


    return resultat
      


















      

def group_list(lst):
    x={}
    for el in x:
        x[el]=lst.count(el)
    x =dict(sorted(x.items(), key=lambda item: item[1], reverse=True))
            
    return x
     
# Driver code
lst = ["a", "a","b", "c", "d", "c", "c", "d"]
print(group_list(lst))