import datetime
import sqlite3

sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())

conn = sqlite3.connect('../data/tv_programs.db')
cur = conn.cursor()


def create_database():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS series (
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


def insert_one_data(nom: str, episode_number: int, season_number: int, diffusion_date: datetime, origin_country: str,
                    broadcast_channel: str, linked_url: str):
    cur.execute("INSERT INTO series (nom, episode_number, season_number, diffusion_date, origin_country, "
                "broadcast_channel, linked_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nom, episode_number, season_number, diffusion_date, origin_country, broadcast_channel, linked_url))
    conn.commit()


if __name__ == '__main__':
    create_database()
    today = datetime.date.today()
    insert_one_data("toto", 1, 2, today, "France", "LivecampusTV", "livecampus.fr")
    insert_one_data("titi", 2, 14, today, "France", "LivecampusTV", "livecampus.fr")

