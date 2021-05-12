from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os


class Main:
    def __init__(
            self,
            url: str,
            path: str
    ):
        self.url = url
        self.path = path if path[-1] == '/' else path + '/'

        self.client_session = ''

        self.images_list = []
        self.links_len = 0
        self.links_got = 0
        self.images_len = 0
        self.image_downloaded = 0

    async def stop(self):
        await self.client_session.close()

    @staticmethod
    def __progress_bar(
            iteration: int,
            total: int,
            prefix: str
    ):
        f = int(100 * iteration // total)
        bar = '█' * f + ' ' * (100 - f)

        print(f'\r{prefix} [{bar}] {str(round(100 * (iteration / float(total)), 2))}%', end="")
        if iteration == total:
            print()

    @staticmethod
    async def __limit_task(
            number: int,
            *tasks
    ):
        semaphore = asyncio.Semaphore(number)

        async def sem_task(task):
            async with semaphore:
                await task

        await asyncio.gather(*(sem_task(task) for task in tasks))

    async def __parse_url(self, url: str):
        async with self.client_session.get(url) as r:
            links = BeautifulSoup(
                await r.text(),
                "html.parser"
            )

        get_all_img_tags = links.findAll("img")

        for link in get_all_img_tags:
            href = str(link.get('src'))

            if href.startswith('https://images') or href.startswith('https://mfiles'):
                images_link_list_split = href.split('/')
                images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
                images_name_file = images_name_file_thumb.split('-')[len(images_name_file_thumb.split('-')) - 1]

                href = href.replace(images_name_file_thumb, '') + images_name_file

                self.images_list.append([href, images_name_file])

        self.links_got += 1
        self.__progress_bar(self.links_got, self.links_len, 'Récupération des liens des images')

    async def __download(self, element: list):
        if os.path.isfile(self.path + element[1]) is False:
            async with self.client_session.get(element[0]) as r:
                with open(self.path + element[1], 'wb') as f:
                    async for data in r.content.iter_chunked(1024):
                        f.write(data)

        self.image_downloaded += 1
        self.__progress_bar(self.image_downloaded, self.images_len, 'Téléchargement des images')

    async def start(self):
        self.client_session = aiohttp.ClientSession()

        if os.path.exists(self.path) is False:
            os.mkdir(self.path)

        pages_list = []
        page_char = "&" if "https://mobile.alphacoders.com/" not in self.url else "?"

        async with self.client_session.get(f'{self.url}{page_char}page=1') as r:
            all_links = BeautifulSoup(
                await r.text(),
                "html.parser"
            ).find_all("a", href=True)

        for link in all_links:
            href = str(link.get('href'))

            if href.find('page') >= 0:
                try:
                    pages_list.append(href.split('&page=')[1])
                except IndexError:
                    pages_list.append(href.split(f'?page=')[1])

        page_number = pages_list[int(max(pages_list))]

        all_pages = [f'{self.url}{page_char}page={str(i)}' for i in range(int(page_number) + 1)]
        self.links_len = len(all_pages)

        self.__progress_bar(0, self.links_len, 'Récupération des liens des images')
        await self.__limit_task(15, *[self.__parse_url(url) for url in all_pages])

        self.images_len = len(self.images_list)

        self.__progress_bar(0, self.images_len, 'Téléchargement des images')
        await self.__limit_task(10, *[self.__download(element) for element in self.images_list])

        await self.stop()


async def main():
    client = None
    try:
        url_base = input(
            "Veuillez rentrez l'url de téléchargement (ex : https://wall.alphacoders.com/search.php?search=sword+art+online). > "
        ).replace(' ', '')

        path = input("Veuillez rentrez le dossier d'enregistrement des images (ex : /home/asthowen/download/). > ")

        client = Main(url_base, path)

        await client.start()
    except KeyboardInterrupt:
        if client is not None:
            await client.close()
    except FileNotFoundError:
        print("Ce dossier n'existe pas.")


if __name__ == '__main__':
    asyncio.run(
        main()
    )
