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
    total_episodes = len(calendrier_episodes)
    if total_episodes > limit:
        total_episodes = limit

    # defini une liste vide pour y mettre chaque épisode scrappé
    all_episodes = []

    # boucle sur chaque element HTML avec la class "calendrier_episodes"
    for index, calendrier_episode in enumerate(calendrier_episodes[:limit]):
        # déclare le temps en début de boucle pour l'estimation
        current = time.time()

        # print la progression
        print("progression : " + format(index + 1) + " / " + format(total_episodes))

        # construit l'url de l'épisode
        url = "https://www.spin-off.fr/" + calendrier_episode.find_all("a")[1].get("href")

        # scrappe la page de l'épisode
        response = requests.get(url)
        content = response.content
        page = BeautifulSoup(content, 'html.parser')

        # récupère les données sur les balises meta dans la div avec la class "main_table"
        nom_serie = page.find('div', class_=['main_table']).find("meta", itemprop="partOfTVSeries").get("content")
        nom_episode = page.find('div', class_=['main_table']).find("meta", itemprop="name").get("content")
        saison_num = page.find('div', class_=['main_table']).find("meta", itemprop="partOfSeason").get("content")
        episode_num = page.find('div', class_=['main_table']).find("meta", itemprop="episodeNumber").get("content")

        # traite les textes dans les spans avec split, replace et strip
        date_diffusion = None  # Initialiser la date de diffusion à None par défaut
        origine = None
        plateform = None
        infos_div = page.find('div', class_=['episode_infos_episode_chaine'])
        if infos_div:
            spans = infos_div.find_all("span")
            if len(spans) > 1:
                origine_img = spans[1].find("img")
                origine = origine_img.get("alt") if origine_img else None
                plateform_text = spans[1].text.split("Diffusé sur")[1].replace('Diffusé sur', '').strip()
                plateform = plateform_text if plateform_text else None
                start_date_meta = spans[0].find("meta", itemprop="startDate")
                date_diffusion = start_date_meta.get("content") if start_date_meta else None

        # ajoute un dictionnaire de l'épisode dans la liste des épisodes
        all_episodes.append({
            "nom_serie": nom_serie,
            "numero de lepisode": episode_num,
            "numero de la saison": saison_num,
            "date diffusion": date_diffusion,
            "origine": origine,
            "plateform": plateform,
            "url episode": url
        })

        # déclare le temps en fin de boucle et fait la différence avec le temps en début de boucle, la différence en seconde est multipliée par le reste d'épisode a scrapper et divisée par 60 pour donner des minutes
        end = time.time()
        diff = end - current
        minute = round((round(diff, 2) * (total_episodes - (index + 1))) / 60, 2)
        print("Il reste environ " + format(minute) + " minutes")

    return all_episodes

# Appel de la fonction pour obtenir les épisodes
episodes = get_all_episode(10)
print(episodes)

# Appel de la fonction pour enregistrer les épisodes dans un fichier CSV
save_episodes_to_csv(episodes, 'src/data/files/episodes.csv')
