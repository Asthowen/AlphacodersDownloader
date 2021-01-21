from bs4 import BeautifulSoup
import requests
import sys
import os

url_base = input("Veuillez rentrez l'url de base (ex : https://wall.alphacoders.com/search.php?search=sword+art+online). > ")
path = input("Veuillez rentrez le dossier d'enregistrement des images (ex : /home/jean_eude/test/). > ")
path = path if path[-1] == '/' else path + '/'

if os.path.exists(path) is False:
    os.mkdir(path)

sys.stdout.write('\r' + 'Récupération du nombre de pages.')
sys.stdout.flush()

soup = BeautifulSoup(requests.get(url_base + '&page=1').content, "html.parser")
all_links = soup.find_all("a")

pages_list = []

for link in all_links:

    href = str(link.get('href'))

    if href.find('page') >= 0:
        pages_list.append(href.split('&page=')[1])

page_number = pages_list[int(max(pages_list))]

sys.stdout.write('\r' + str(page_number) + " pages trouvées.")
sys.stdout.flush()

page_check = 1

all_pages = []

while page_check < int(page_number) + 1:
    all_pages.append(url_base + '&page=' + str(page_check))
    page_check += 1


images_list = []

sys.stdout.write('\r' + str(page_number) + " Lancement de la récupération des liens de toutes les images.")
sys.stdout.flush()

counter_page_link = 1

for page_link in all_pages:
    soup = BeautifulSoup(requests.get(page_link).text, "html.parser")

    get_all_img_tags = soup.findAll("img")

    for link in get_all_img_tags:
        href = str(link.get('src'))
        if href.startswith('https://images'):
            images_link_list_split = href.split('/')
            images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
            images_name_file = images_name_file_thumb.split('-')[len(images_name_file_thumb.split('-')) - 1]

            href = href.replace(images_name_file_thumb, '') + images_name_file

            images_list.append([href, images_name_file])
            sys.stdout.write('\r' + str(counter_page_link) + " liens trouvé.")
            sys.stdout.flush()

            counter_page_link += 1

image_list_len = len(images_list)

sys.stdout.write('\r' + f'Récupération des images terminé ({images_list} images trouvées).')
sys.stdout.flush()


sys.stdout.write('\r' + 'Lancement du téléchargement des images.')
sys.stdout.flush()

counter = 1

for image_link in images_list:
    if os.path.isfile(path + image_link[1]) is False:
        response = requests.get(image_link[0], stream=True).content
        with open(path + image_link[1], 'wb') as out_file:
            out_file.write(response)

    sys.stdout.write('\r' + f"{str(counter)}/{str(image_list_len)}")
    sys.stdout.flush()
    counter += 1

sys.stdout.write('\r' + 'Téléchargement terminé !')
sys.stdout.flush()