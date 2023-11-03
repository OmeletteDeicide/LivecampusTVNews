
import requests
from bs4 import BeautifulSoup
import time  

def get_all_episode(limit=500):

    # on récupère le code html de l'url
    url = "https://www.spin-off.fr/calendrier_des_series.html"
    response = requests.get(url)
    content = response.content

    # On parse la page avec BeautifulSoup
    page = BeautifulSoup(content, 'html.parser')

    # selection des elements avec la class "calendrier_episodes" qui contient l'url de la page de l'épisode
    calendrier_episodes = page.find_all(class_="calendrier_episodes")

    # défini le total d'épisodes sur la page
    total_episodes=len(calendrier_episodes)
    if(total_episodes>limit):
        total_episodes=limit


    # defini une liste vide pour y mettre chaque épisode scrappé
    all_episodes = []

    # boucle sur chaque element HTML avec la class "calendrier_episodes"
    for index, calendrier_episode in enumerate(calendrier_episodes[:limit]):
        # déclare le temps en début de boucle pour l'estimation
        current = time.time()



        # print la progression 
        print("progression : "+format(index+1)+" / "+ format(total_episodes))

        # construit l'url de l'épisode
        url = "https://www.spin-off.fr/"+calendrier_episode.find_all("a")[1].get("href")

        # scrappe la page de l'épisode
        response = requests.get(url)
        content = response.content
        page = BeautifulSoup(content, 'html.parser')
        
        # récupère les données sur les balises meta dans la div avec la class "main_table"
        nom_serie= page.find('div',class_=['main_table']).find("meta", itemprop="partOfTVSeries").get("content")
        nom_episode = page.find('div',class_=['main_table']).find("meta", itemprop="name").get("content")
        saison_num = page.find('div',class_=['main_table']).find("meta", itemprop="partOfSeason").get("content")
        episode_num = page.find('div',class_=['main_table']).find("meta", itemprop="episodeNumber").get("content")
        date_publication = page.find('div',class_=['main_table']).find("meta", itemprop="datePublished").get("content")
        
        # traite les textes dans les spans avec split, replace et strip
        date_diffusion = page.find('div',class_=['episode_infos_episode_chaine']).text.split("Diffusé sur")[0].replace('Diffusé le ', '').strip()
        chaine_plateform = page.find('div',class_=['episode_infos_episode_chaine']).text.split("Diffusé sur")[1].replace('Diffusé sur ', '').strip()

        # récupère le pays avec la source de l'image du drapeau
        origin = page.find('div',class_=['episode_infos_episode_chaine']).find_all("span")[1].find("img").get("src").split("/")[-1].strip(".png").upper()

        # ajoute un dictionnaire de l'épisode dans la liste des épisodes
        all_episodes.append({
            "origine":origin,
            "nom série":nom_serie,
            "nom épisode":nom_episode,
            "numéro saison":saison_num,
            "numéro episode":episode_num,
            "plateform":chaine_plateform,
            "date diffusion":date_diffusion,
            "url":url
            })
        
        # déclare le temps en fin de boucle et fait la différence avec le temps en début de boucle, la différence en seconde est multiplié par le reste d'épisode a scrapper et diviser par 60 pour donner des minutes
        end = time.time()
        diff = end - current
        minute =round((round(diff,2)*(total_episodes-(index+1)))/60,2)
        print("Il reste environ "+format(minute)+" minutes")


    print(all_episodes)
    return all_episodes

get_all_episode(10)