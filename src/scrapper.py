import requests
from bs4 import BeautifulSoup
import datetime


def get_all_episode(by_date=False,by_chaine=False,with_time=False):
    # si la date n'est pas donné on prend la date actuel
    if(by_date == False):
        by_date = datetime.datetime.now()
        by_date=by_date.strftime("%Y-%m")
    # création liste pour y mettre chaque épisode
    all_episodes = []
    # on récupère le code html de l'url
    url = "https://www.spin-off.fr/calendrier_des_series.html?date="+by_date
    response = requests.get(url)
    content = response.content
    # On parse la page avec BeautifulSoup
    page = BeautifulSoup(content, 'html.parser')

    # on récupère les td avec comme class "floatleftmobile"
    floatleftmobiles  = page.find_all('td',class_=['floatleftmobile'])
 
    # boucle sur chaque td
    for floatleftmobile in floatleftmobiles:
        
        # si le td font partis du mois en court
        if(floatleftmobile.find("div",class_=['div_jour'])):

            # on récupère la date dans l'id de la div avec la class "div_jour"
            jour = floatleftmobile.find("div",class_=['div_jour']).get("id").strip("jour_")

            # selection des elements avec la class "calendrier_episodes" qui contient les infos de l'épisode
            calendrier_episodes = floatleftmobile.find_all(class_="calendrier_episodes")

            # boucle sur les élement avec la class "calendrier_episodes"
            for calendrier_episode in calendrier_episodes:

                # on obtient les infos a l'aide de find_previous_sibling(), split(), strip()...
                origine = calendrier_episode.find_previous_sibling().find_previous_sibling().get("alt")
                chaine = calendrier_episode.find_previous_sibling().get("alt")
                str_infos = calendrier_episode.find_all("a")[1].get("title")
                url = "https://www.spin-off.fr/"+calendrier_episode.find_all("a")[1].get("href")
                name = str_infos.split("saison")[0].strip()
                numero_saison = str_infos.split("saison")[1].split("episode")[0].strip()
                numero_episode = str_infos.split("saison")[1].split("episode")[1].strip()

                # on stock les infos dans un dictionnaire
                episode ={
                "origine":origine,
                "nom série":name,
                "numéro saison":numero_saison,
                "numéro episode":numero_episode,
                "chaine":chaine,
                "date diffusion":jour,
                "url":url
                }

                # si le fitre by_chaine est demandé
                if(by_chaine != False):

                    # la chaine de l'épisode correspond au filtre
                    if(by_chaine==chaine):

                        # si with_time est True on va chercher la durée de l'épisode seulement si le filtre by_chaine est activé sinon requêtes trop longue
                        if(with_time != False):
                            response = requests.get(url)
                            content = response.content
                            page = BeautifulSoup(content, 'html.parser')
                            duree_episode = page.find('div',class_=['episode_infos_episode_format']).text.replace("\n","").replace("\t","").strip().split("minutes")[0]
                            episode["durée"]=duree_episode
                        # on ajoute l'épisode au dictionnaire
                        all_episodes.append(episode)
                else:
                    # si aucun filtre et parametre et activé on ajoute l'épisode au dictionnaire sans la durée
                    all_episodes.append(episode)

    # return les épisodes
    return all_episodes



#episodes = get_all_episode("2023-10","France 2",True)
