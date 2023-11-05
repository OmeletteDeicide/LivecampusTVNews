
from scrapper import get_all_episode
from algo import infos_episode
from src.model import create_database, insert_multiple_datas, insert_multiple_datas_with_duration


if __name__ == '__main__':
    # Scraping 1/2
    episodes_octobre = get_all_episode("2023-10")
    print(episodes_octobre)

    # Scraping 2/2
    episodes_octobre_with_time = get_all_episode("2023-10","Apple tv+",True)
    print(episodes_octobre_with_time)

    # Algo
    infos = infos_episode(episodes_octobre)
    print(infos)

    # Algo 1/2
    infos["episodes_par_chaine"]
    infos["episodes_par_pays"]
    infos["mots_recurrents"]

    # Algo 2/2
    infos["chaine_jour_consecutif_diffusion"]

    # Aller voir -> data/databases/database.db pour voir les infos SQL
    # SQL 1/2
    create_database()
    insert_multiple_datas(get_all_episode())

    # SQL 2/2
    insert_multiple_datas_with_duration(get_all_episode(False, "NBC", True))
