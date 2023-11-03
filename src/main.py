import requests
from bs4 import BeautifulSoup
import time

import csv

def save_episodes_to_csv(episodes, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        # Écrire l'en-tête du CSV
        writer.writerow(["nom série", "numero de lepisode", "numero de la saison", "date diffusion", "origine", "plateform", "url episode"])

        for episode in episodes:
            writer.writerow([
                episode.get("nom_serie", ""),
                episode.get("numero de lepisode", ""),
                episode.get("numero de la saison", ""),
                episode.get("date diffusion", ""),
                episode.get("origine", ""),
                episode.get("plateform", ""),
                episode.get("url episode", "")
            ])

def get_all_episode(duree=False):
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
                print(index)
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
                "url":url
                }
                if(duree):
                    response = requests.get(url)
                    content = response.content
                    page = BeautifulSoup(content, 'html.parser')
                    
                    #nom_episode = page.find('div',class_=['main_table']).find("meta", itemprop="name").get("content")
                    duree_episode = page.find('div',class_=['episode_infos_episode_format']).text.replace("\n","").replace("\t","").strip()
                    episode["durée"] = duree_episode
                    all_episodes.append(episode)
                    return all_episodes
                all_episodes.append(episode)
    return all_episodes

#get_all_episode()
