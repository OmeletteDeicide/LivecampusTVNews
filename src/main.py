
from scrapper import get_all_episode
from episodes_to_csv import save_episodes_to_csv
from algo import infos_episode

# Scraping 1/2 
episodes_octobre = get_all_episode("2023-10")

# Scraping 2/2 
episodes_octobre_with_time = get_all_episode("2023-10","Apple tv+",True)

# Algo
infos = infos_episode(episodes_octobre)

# Algo 1/2
infos["episodes_par_chaine"]
infos["episodes_par_pays"]
infos["mots_recurrents"]

# Algo 2/2
infos["chaine_jour_consecutif_diffusion"]

