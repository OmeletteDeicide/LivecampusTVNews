# function qui prend en argument la liste des épisodes et qui return les infos épisodes par chaine, pays, diffusion jours consecutif par chaine et les mots récurrents par titre de serie

def infos_episode(liste_episodes):
    # création dictionnaire pour y inserer les infos
    resultat =  {
                "episodes_par_chaine":{},
                "episodes_par_pays":{},
                "chaine_jour_consecutif_diffusion":{},
                "mots_recurrents":{}
                
            }
    # liste de chaque titre sans doublon
    liste_titres=[]

    # liste des mots dans les titres
    liste_mots=[]
    previous_day = False
    # boucle sur chaque episode
    for episode in liste_episodes:
        if(previous_day==False):
            previous_day=episode["date diffusion"]
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

        # declare jours diffusion en int 
        jours = int(episode["date diffusion"].split("-")[0])

        # ajoute les jours de diffusion sans doublon pour chaque chaine : {'France 2':[1,3,4,12]}
        if episode["chaine"] not in resultat["chaine_jour_consecutif_diffusion"]:
            resultat["chaine_jour_consecutif_diffusion"][episode["chaine"]]=[jours]
        elif (jours not in resultat["chaine_jour_consecutif_diffusion"][episode["chaine"]]):
            resultat["chaine_jour_consecutif_diffusion"][episode["chaine"]].append(jours)

    # boucle sur chaque chaine 
    for chaine in resultat["chaine_jour_consecutif_diffusion"]:

        # déclaration de previous_day, mémoire tampon du jours  
        previous_day=0

        # déclaration de jours_consecutif, variable qu'on va incrémenter si previous_day+1 == day
        jours_consecutif = 0

        # déclaration de max_jours_consecutif, variable qui va garder la valeur max de jours_consecutif
        max_jours_consecutif = 0

        # boucle sur chaque jours de diffusion d'une chaine, pour ainsi avoir le plus de jours consecutif d'une chaine
        for day in resultat["chaine_jour_consecutif_diffusion"][chaine]:
            if(previous_day+1==day):
                jours_consecutif +=1
            else:
                jours_consecutif=1
            if(jours_consecutif>max_jours_consecutif):
                max_jours_consecutif=jours_consecutif
            previous_day=day
        # on insere max_jours_consecutif à la chaine 
        resultat["chaine_jour_consecutif_diffusion"][chaine]=max_jours_consecutif
        
    # boucle sur tout les titres
    for titre in liste_titres:

        # boucle sur chaque mot de chque titre pour inserer le mot dans la liste "liste_mots" et mettre à jour dans le dictionnaire la récurrence du mot dans la liste "liste_mots"
        for mot in titre.split(" "):
            liste_mots.append(mot)
            resultat["mots_recurrents"][mot]=liste_mots.count(mot)

    # tri chaque dictionnaire dans l'ordre décroissant 
    resultat["episodes_par_chaine"] =dict(sorted(resultat["episodes_par_chaine"].items(), key=lambda item: item[1], reverse=True))
    resultat["episodes_par_pays"] =dict(sorted(resultat["episodes_par_pays"].items(), key=lambda item: item[1], reverse=True))
    resultat["chaine_jour_consecutif_diffusion"] =dict(sorted(resultat["chaine_jour_consecutif_diffusion"].items(), key=lambda item: item[1], reverse=True))
    resultat["mots_recurrents"] =dict(sorted(resultat["mots_recurrents"].items(), key=lambda item: item[1], reverse=True))

    return resultat