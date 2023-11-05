import datetime
import sqlite3

from src.scrapper import get_all_episode

sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())

conn = sqlite3.connect('./data/databases/database.db')
cur = conn.cursor()


def create_database():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS episode (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            episode_number INTEGER,
            season_number INTEGER,
            diffusion_date DATE,
            origin_country TEXT,
            broadcast_channel TEXT,
            linked_url TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS duration (
            duree INTEGER,
            episode_id INTEGER,
            FOREIGN KEY (episode_id) REFERENCES episode(id)
        )
    ''')

    conn.commit()


def insert_one_data(nom: str, episode_number: int, season_number: int, diffusion_date: datetime.date,
                    origin_country: str,
                    broadcast_channel: str, linked_url: str):
    cur.execute("INSERT INTO episode (nom, episode_number, season_number, diffusion_date, origin_country, "
                "broadcast_channel, linked_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nom, episode_number, season_number, diffusion_date, origin_country, broadcast_channel, linked_url))
    conn.commit()


def insert_multiple_datas(list_datas):
    i = 1
    for data in list_datas:
        cur.execute("INSERT INTO episode (nom, episode_number, season_number, diffusion_date, origin_country, "
                    "broadcast_channel, linked_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data['nom série'], data['numéro episode'], data['numéro saison'], data['date diffusion'],
                     data['origine'], data['chaine'], data['url']))

    conn.commit()


def insert_multiple_datas_with_duration(list_datas):
    i = 1
    for data in list_datas:
        cur.execute("INSERT INTO episode (nom, episode_number, season_number, diffusion_date, origin_country, "
                    "broadcast_channel, linked_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data['nom série'], data['numéro episode'], data['numéro saison'], data['date diffusion'],
                     data['origine'], data['chaine'], data['url']))
        cur.execute(
            "SELECT id FROM episode WHERE nom=? AND episode_number=? AND season_number=? AND diffusion_date=?;",
            (data['nom série'], data['numéro episode'], data['numéro saison'], data['date diffusion']))
        episode_id = cur.fetchone()
        cur.execute("INSERT INTO duration (duree, episode_id) VALUES (?, ?)",
                    (data['durée'], episode_id[0]))

    conn.commit()
