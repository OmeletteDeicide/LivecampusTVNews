import csv

from scrapper import get_all_episode


def save_episodes_to_csv(episodes, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        # Écrire l'en-tête du CSV
        writer.writerow(["nom série", "numéro episode", "numéro saison", "date diffusion", "origine", "plateform", "url"])

        for episode in episodes:
            writer.writerow([
                episode.get("nom série", ""),
                episode.get("numéro episode", ""),
                episode.get("numéro saison", ""),
                episode.get("date diffusion", ""),
                episode.get("origine", ""),
                episode.get("plateform", ""),
                episode.get("url", "")
            ])
episodes = get_all_episode()

save_episodes_to_csv(episodes, 'src/data/files/episodes.csv')