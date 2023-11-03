import requests
from bs4 import BeautifulSoup

def get_all_episode():
    all_episodes = []
    # on récupère le code html de l'url
    url = "https://www.spin-off.fr/calendrier_des_series.html"
    response = requests.get(url)
    content = response.content
    # On parse la page avec BeautifulSoup
    page = BeautifulSoup(content, 'html.parser')
    floatleftmobiles  = page.find_all('td',class_=['floatleftmobile'])
 
    for floatleftmobile in floatleftmobiles:
        if(floatleftmobile.find("div",class_=['div_jour'])):
            #jour
            jour = floatleftmobile.find("div",class_=['div_jour']).get("id").strip("jour_")
            # selection des elements avec la class "calendrier_episodes" qui contient l'url de la page de l'épisode
            calendrier_episodes = floatleftmobile.find_all(class_="calendrier_episodes")
            for index, calendrier_episode in enumerate(calendrier_episodes):
                #origine
                origine = calendrier_episode.find_previous_sibling().find_previous_sibling().get("alt")
                chaine = calendrier_episode.find_previous_sibling().get("alt")
                str_infos = calendrier_episode.find_all("a")[1].get("title")
                url = "https://www.spin-off.fr/"+calendrier_episode.find_all("a")[1].get("href")
                name = str_infos.split("saison")[0].strip()
                numero_saison = str_infos.split("saison")[1].split("episode")[0].strip()
                numero_episode = str_infos.split("saison")[1].split("episode")[1].strip()
 
                episode ={
                "origine":origine,
                "nom série":name,
                "numéro saison":numero_saison,
                "numéro episode":numero_episode,
                "plateform":chaine,
                "date diffusion":jour,
                "url":url,
                "durée": ""
                }
                if(chaine=="Apple TV+"):
                    response = requests.get(url)
                    content = response.content
                    page = BeautifulSoup(content, 'html.parser')
                    
                    #nom_episode = page.find('div',class_=['main_table']).find("meta", itemprop="name").get("content")
                    duree_episode = page.find('div',class_=['episode_infos_episode_format']).text.replace("\n","").replace("\t","").strip()
                    episode["durée"] = duree_episode
                all_episodes.append(episode)
    return all_episodes

