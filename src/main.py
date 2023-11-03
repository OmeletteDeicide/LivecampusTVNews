
from scrapper import get_all_episode
from episodes_to_csv import save_episodes_to_csv
from algo import infos_episode


episodes = get_all_episode()
infos = infos_episode(episodes)
print(infos)