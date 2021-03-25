from bs4 import BeautifulSoup
import requests
import os


def progress_bar(iteration, total, prefix=''):
    filled_length = int(100 * iteration // total)
    bar = '█' * filled_length + ' ' * (100 - filled_length)
    print(f'\r{prefix} [{bar}] {str(round(100 * (iteration / float(total)), 2))}%', end="")
    if iteration == total:
        print()


try:
    url_base = input(
        "Veuillez rentrez l'url de téléchargement (ex : https://wall.alphacoders.com/search.php?search=sword+art+online). > ").replace(
        ' ', '')

    path = input("Veuillez rentrez le dossier d'enregistrement des images (ex : /home/asthowen/download/). > ")
    path = path if path[-1] == '/' else path + '/'

    if os.path.exists(path) is False:
        os.mkdir(path)

    print('Récupération du nombre de pages.')

    page_char = "&" if "https://mobile.alphacoders.com/" not in url_base else "?"

    soup = BeautifulSoup(requests.get(f'{url_base}{page_char}page=1').content, "html.parser")
    all_links = soup.find_all("a")

    pages_list = []

    progress_bar(0, len(all_links), prefix='Récuparations des pages :')

    for i, link in enumerate(all_links):
        href = str(link.get('href'))

        if href.find('page') >= 0:
            try:
                pages_list.append(href.split('&page=')[1])
            except IndexError:
                pages_list.append(href.split(f'?page=')[1])

        progress_bar(i + 1, len(all_links), prefix='Récuparations des pages :')

    page_number = pages_list[int(max(pages_list))]

    print(f'Pages trouvées : {str(page_number)}')

    all_pages = []

    for i in range(int(page_number) + 1):
        all_pages.append(f'{url_base}{page_char}page={str(i)}')

    images_list = []

    print('Lancement de la récupération des liens de toutes les images.')

    counter_page_link = 1

    progress_bar(0, len(all_pages), prefix='Récuparations des liens des images :')

    for i, page_link in enumerate(all_pages):
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

                counter_page_link += 1
        progress_bar(i + 1, len(all_pages), prefix='Récuparations des liens des images :')

    image_list_len = len(images_list)

    print(f'Récupération des images terminé ({str(image_list_len)} images trouvées).')

    print('Lancement du téléchargement des images.')

    progress_bar(0, image_list_len, prefix='Téléchargement des images :')

    for i, image_link in enumerate(images_list):
        if os.path.isfile(path + image_link[1]) is False:
            with open(path + image_link[1], 'wb') as f:
                f.write(requests.get(image_link[0], stream=True).content)

        progress_bar(i + 1, image_list_len, prefix='Téléchargement des images :')

    print('Téléchargement terminé !')
except KeyboardInterrupt:
    pass
