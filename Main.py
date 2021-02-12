from bs4 import BeautifulSoup
import requests
import sys
import os


def clear_previous_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")


def log(log: str):
    clear_previous_line()
    print(log)


url_base = input(
    "Veuillez rentrez l'url de base (ex : https://wall.alphacoders.com/search.php?search=sword+art+online or https://mobile.alphacoders.com/by-sub-category/227264). > ").replace(
    ' ', '')

clear_previous_line()

path = input("Veuillez rentrez le dossier d'enregistrement des images (ex : /home/jean_eude/test/). > ")
path = path if path[-1] == '/' else path + '/'

if os.path.exists(path) is False:
    os.mkdir(path)

log('Récupération du nombre de pages.')

page_char = "&" if "https://mobile.alphacoders.com/" not in url_base else "?"

soup = BeautifulSoup(requests.get(f'{url_base}{page_char}page=1').content, "html.parser")
all_links = soup.find_all("a")

pages_list = []

for link in all_links:

    href = str(link.get('href'))

    if href.find('page') >= 0:
        try:
            pages_list.append(href.split('&page=')[1])
        except:
            pages_list.append(href.split(f'?page=')[1])

try:
    page_number = pages_list[int(max(pages_list))]
except:
    log("Vous n'avez pas accès au site.")
    sys.exit()

log(f'Pages trouvées : {str(page_number)}.')

page_check = 1

all_pages = []

while page_check < int(page_number) + 1:
    all_pages.append(f'{url_base}{page_char}page={str(page_check)}')
    page_check += 1

images_list = []

log('Lancement de la récupération des liens de toutes les images.')

counter_page_link = 1

for page_link in all_pages:
    soup = BeautifulSoup(requests.get(page_link).text, "html.parser")

    get_all_img_tags = soup.findAll("img")

    for link in get_all_img_tags:
        href = str(link.get('src'))
        if href.startswith('https://images') or href.startswith('https://mfiles'):
            images_link_list_split = href.split('/')
            images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
            images_name_file = images_name_file_thumb.split('-')[len(images_name_file_thumb.split('-')) - 1]

            href = href.replace(images_name_file_thumb, '') + images_name_file

            images_list.append([href, images_name_file])
            log(f'Liens trouvé : {str(counter_page_link)}.')

            counter_page_link += 1

image_list_len = len(images_list)

log(f'Récupération des images terminé ({str(image_list_len)} images trouvées).')

log('Lancement du téléchargement des images.')

counter = 1

for image_link in images_list:
    if os.path.isfile(path + image_link[1]) is False:
        response = requests.get(image_link[0], stream=True).content
        with open(path + image_link[1], 'wb') as out_file:
            out_file.write(response)

    log(f'{str(counter)}/{str(image_list_len)}')

    counter += 1

log('Téléchargement terminé !')