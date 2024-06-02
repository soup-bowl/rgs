import sys
import requests
from bs4 import BeautifulSoup

# URL of the NGINX indexed list
BASE_URL = "https://thumbnails.libretro.com/"

def fetch_console_url(console_url, subdir):
	try:
		response = requests.get(console_url + subdir, timeout=5)
		response.raise_for_status()
		return response
	except requests.exceptions.HTTPError as e:
		if e.response.status_code == 404:
			return None
		print(f"Error fetching {subdir} URL: {e}")
		sys.exit(2)
	except requests.exceptions.RequestException as e:
		print(f"Error fetching {subdir} URL: {e}")
		sys.exit(2)

def get_game_list(base_url):
	try:
		response = requests.get(base_url, timeout=10)
		response.raise_for_status()
	except requests.exceptions.RequestException as e:
		print(f"Error fetching base URL {base_url}: {e}")
		sys.exit(1)

	soup = BeautifulSoup(response.text, 'html.parser')
	game_list = []

	for link in soup.find_all('a'):
		href = link.get('href')
		if '../' not in href and href.endswith('/'):
			console_url = base_url + href
			subdirs = ['Named_Boxarts/', 'Named_Snaps/', 'Named_Titles/']
			console_response = None

			for subdir in subdirs:
				console_response = fetch_console_url(console_url, subdir)
				if console_response:
					break

			if not console_response:
				continue

			console_soup = BeautifulSoup(console_response.text, 'html.parser')

			for game_link in console_soup.find_all('a'):
				game_href = game_link.get('href')
				if '../' not in game_href and (game_href.endswith('.jpg') or game_href.endswith('.png')):
					game_url = console_url + 'Named_Boxarts/' + game_href
					game_list.append(game_url)

	return game_list

def write_game_urls_to_file(game_list, output_file):
	with open(output_file, 'w', encoding="utf-8") as file:
		for game_url in game_list:
			file.write(f"{game_url}\n")


games = get_game_list(BASE_URL)
write_game_urls_to_file(games, "gameart.txt")
