from alphacoders_downloader.utils import limit_task, clear_line, print_error
from alphacoders_downloader.cursor import HiddenCursor, show
from alphacoders_downloader.progress_bar import ProgressBar
from bs4 import BeautifulSoup
import setproctitle
import aiofiles
import asyncio
import aiohttp
import shutil
import os


class Main:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path if path[-1] == os.sep else path + os.sep
        self.temp_path = self.path + 'temp' + os.sep

        self.progress_bar: ProgressBar = None
        self.client_session = None
        self.images_list = []
        self.links_len = 0
        self.links_got = 0
        self.images_len = 0
        self.image_downloaded = 0

    async def parse_url(self, url: str):
        async with self.client_session.get(url) as r:
            links = BeautifulSoup(await r.text(), 'html.parser')

        for link in links.findAll('img'):
            href = str(link.get('src'))

            if href.startswith('https://images') or href.startswith('https://mfiles'):
                images_link_list_split = href.split('/')
                images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
                images_name_file = images_name_file_thumb.split('-')[len(images_name_file_thumb.split('-')) - 1]

                self.images_list.append([href.replace(images_name_file_thumb, '') + images_name_file, images_name_file])

        self.links_got += 1
        self.progress_bar.progress(self.links_got)

    async def download(self, element: list):
        if os.path.isfile(self.path + element[1]) is False:
            async with self.client_session.get(element[0]) as r:
                try:
                    async with aiofiles.open(self.temp_path + element[1], 'wb') as f:
                        try:
                            async for data in r.content.iter_chunked(1024):
                                await f.write(data)
                        except asyncio.TimeoutError:
                            self.image_downloaded += 1
                            self.progress_bar.progress(self.image_downloaded)
                            return self.progress_bar.print_error(f"Download of file: {element[0]} has been timeout.")
                except aiohttp.ClientPayloadError:
                    self.image_downloaded += 1
                    self.progress_bar.progress(self.image_downloaded)
                    return self.progress_bar.print_error(f"Download of file: {element[0]} has been ClientPayloadError.")

                if os.path.isfile(self.temp_path + element[1]):
                    shutil.move(self.temp_path + element[1], self.path + element[1])

        self.image_downloaded += 1
        self.progress_bar.progress(self.image_downloaded)

    async def start(self):
        self.client_session = aiohttp.ClientSession()

        if os.path.exists(self.path) is False:
            os.mkdir(self.path)

        if os.path.exists(self.temp_path) is False:
            os.mkdir(self.temp_path)

        pages_list = []
        page_char = '&' if 'https://mobile.alphacoders.com/' not in self.url else '?'

        async with self.client_session.get(f'{self.url}{page_char}page=1', cookies={'AlphaCodersView': 'paged'}) as r:
            all_links = BeautifulSoup(await r.text(), 'html.parser').find_all('a', href=True)

        for link in all_links:
            href = str(link.get('href'))

            if href.find('page') >= 0:
                try:
                    pages_list.append(href.split('&page=')[1])
                except IndexError:
                    pages_list.append(href.split('?page=')[1])

        page_number = pages_list[int(max(pages_list))]

        all_pages = [f'{self.url}{page_char}page={str(i)}' for i in range(int(page_number) + 1)]
        self.links_len = len(all_pages)

        self.progress_bar = ProgressBar(self.links_len, 'Retrieving links from images')
        await limit_task(15, *[self.parse_url(url) for url in all_pages])

        self.images_len = len(self.images_list)

        self.progress_bar.set_progress_bar_parameters(self.images_len, 'Downloading images', 0, True)
        await limit_task(10, *[self.download(element) for element in self.images_list])

        await self.client_session.close()
        shutil.rmtree(self.temp_path)
        print('Completed!')


async def main():
    setproctitle.setproctitle('AlphacodersDownloader')
    url = input(
        'Please enter the download url (e.g. '
        'https://wall.alphacoders.com/search.php?search=sword+art+online). > '
    ).replace(' ', '')
    clear_line()
    path = input("Please enter the folder where the images are saved (e.g. ~/downloads/backgrounds/). > ")
    clear_line()

    with HiddenCursor() as _:
        await Main(url, path).start()


def start():
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print('\nStop the script...')
        show()
    except Exception as e:
        print_error(str(e))
        show()
