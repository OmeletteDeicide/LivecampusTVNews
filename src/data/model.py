import datetime
import sqlite3

from src.scrapper import get_all_episode

sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())

conn = sqlite3.connect('../data/database.db')
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

    conn.commit()


def insert_one_data(nom: str, episode_number: int, season_number: int, diffusion_date: datetime.date,
                    origin_country: str,
                    broadcast_channel: str, linked_url: str):
    cur.execute("INSERT INTO episode (nom, episode_number, season_number, diffusion_date, origin_country, "
                "broadcast_channel, linked_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nom, episode_number, season_number, diffusion_date, origin_country, broadcast_channel, linked_url))
    conn.commit()


def insert_multiple_datas(list_datas):
    for data in list_datas:
        cur.execute("INSERT INTO episode (nom, episode_number, season_number, diffusion_date, origin_country, "
                    "broadcast_channel, linked_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data['nom série'], data['numéro episode'], data['numéro saison'], data['date diffusion'],
                     data['origine'], data['plateform'], data['url']))

    conn.commit()


if __name__ == '__main__':
    create_database()
    today = datetime.date.today()
    insert_multiple_datas(get_all_episode())
