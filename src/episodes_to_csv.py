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

