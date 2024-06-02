import requests
from bs4 import BeautifulSoup
import difflib
import os

# URL of the NGINX indexed list
BASE_URL = "https://thumbnails.libretro.com/"

def get_game_list(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    game_list = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if '../' not in href and href.endswith('/'):
            console_url = base_url + href
            console_response = requests.get(console_url + 'Named_Boxarts/')
            console_soup = BeautifulSoup(console_response.text, 'html.parser')
            
            for game_link in console_soup.find_all('a'):
                game_href = game_link.get('href')
                if '../' not in game_href and (game_href.endswith('.jpg') or game_href.endswith('.png')):
                    game_url = console_url + 'Named_Boxarts/' + game_href
                    game_list.append(game_url)
                    
    return game_list

def write_game_urls_to_file(game_list, output_file):
    with open(output_file, 'w') as file:
        for game_url in game_list:
            file.write(f"{game_url}\n")


game_list = get_game_list(BASE_URL)
write_game_urls_to_file(game_list, "gameart.txt")
