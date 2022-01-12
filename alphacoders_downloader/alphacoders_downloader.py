from alphacoders_downloader.util.utils import limit_tasks, clear_line, print_error
from alphacoders_downloader.util.arguments_builder import ArgumentsBuilder
from alphacoders_downloader.exceptions import WallpapersNotFounds
from alphacoders_downloader.util.cursor import HiddenCursor, show
from alphacoders_downloader.util.progress_bar import ProgressBar
from bs4 import BeautifulSoup
from typing import Union
import setproctitle
import aiofiles
import asyncio
import aiohttp
import shutil
import sys
import os

main_class = None


class Main:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path if path[-1] == os.sep else path + os.sep
        self.temp_path = self.path + 'temp' + os.sep

        self.progress_bar: Union[ProgressBar, None] = None
        self.client_session = None
        self.images_list = []
        self.links_len = 0
        self.links_got = 0
        self.images_len = 0
        self.image_downloaded = 0

    async def parse_url(self, url: str):
        async with self.client_session.get(url) as r:
            page = BeautifulSoup(await r.text(), 'html.parser')

        find_images_urls = page.find('div', attrs={'id': 'big_container'})

        if find_images_urls is None:
            raise WallpapersNotFounds(url)
        else:
            for link in find_images_urls.find_all('img'):
                href = str(link.get('src'))

                if href.startswith('https://images') or href.startswith('https://mfiles'):
                    images_link_list_split = href.split('/')
                    images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
                    images_name_file = images_name_file_thumb.split('-')[len(images_name_file_thumb.split('-')) - 1]

                    self.images_list.append(
                        [href.replace(images_name_file_thumb, '') + images_name_file, images_name_file]
                    )

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
            os.makedirs(self.path)

        if os.path.exists(self.temp_path) is False:
            os.makedirs(self.temp_path)

        pages_list = []
        page_char = '&' if 'https://mobile.alphacoders.com/' not in self.url else '?'

        async with self.client_session.get(f'{self.url}{page_char}page=1', cookies={'AlphaCodersView': 'paged'}) as r:
            all_links = BeautifulSoup(await r.text(), 'html.parser').find_all('a', href=True)

        for link in all_links:
            href = str(link.get('href'))

            if 'page' in href:
                try:
                    href_spliced = href.split('&page=')[1]
                    if href_spliced not in pages_list:
                        pages_list.append(href_spliced)
                except IndexError:
                    href_spliced = href.split('?page=')[1]
                    if href_spliced not in pages_list:
                        pages_list.append(href_spliced)

        if pages_list:
            all_pages = [f'{self.url}{page_char}page={str(i)}' for i in range(int(max(pages_list)) + 1)]
            self.links_len = len(all_pages)

            self.progress_bar = ProgressBar(self.links_len, 'Retrieving links from images')
            await limit_tasks(15, *[self.parse_url(url) for url in all_pages])
        else:
            self.progress_bar = ProgressBar(1, 'Retrieving links from images')
            await self.parse_url(self.url)

        self.images_len = len(self.images_list)
        self.progress_bar.set_progress_bar_parameters(self.images_len, 'Downloading wallpapers', 0, True)
        await limit_tasks(10, *[self.download(element) for element in self.images_list])

        await self.client_session.close()
        shutil.rmtree(self.temp_path)
        print('\033[1mCompleted!\033[0m')


class CommandsHandler:
    @staticmethod
    async def download(command_return: dict):
        wallpapers_url = command_return['args'][command_return['args'].index('-S') + 1]
        if 'https://' not in wallpapers_url and 'alphacoders.com' not in wallpapers_url:
            print_error("This URL isn't correct.")
            sys.exit()
        path_to_download = command_return['args'][command_return['args'].index('-P') + 1]
        if os.access(os.path.dirname(path_to_download), os.W_OK) is False:
            print_error("This path isn't correct.")
            sys.exit()

        global main_class
        main_class = Main(wallpapers_url, path_to_download)
        await main_class.start()

    @staticmethod
    def get_version(_):
        from alphacoders_downloader import __version__, __license__

        version_text = f'\033[1mAlphacodersDownloader {__version__}\033[0m\n'
        version_text += f'Created by \033[1mAsthowen\033[0m - \033[1mcontact@asthowen.fr\033[0m\n'
        version_text += f'License: \033[1m{__license__}\033[0m'

        print(version_text)


async def main():
    setproctitle.setproctitle('AlphacodersDownloader')

    if len(sys.argv) <= 1:
        url = ''
        while 'https://' not in url and 'alphacoders.com' not in url:
            url = input(
                'Please enter the download url (e.g. '
                'https://wall.alphacoders.com/search.php?search=sword+art+online). > '
            ).replace(' ', '')
            clear_line()

        path = ''
        while os.access(os.path.dirname(path), os.W_OK) is False:
            path = input('Please enter the folder where the images are saved (e.g. ~/downloads/wallpapers/). > ')
            clear_line()

        with HiddenCursor() as _:
            global main_class
            main_class = Main(url, path)
            await main_class.start()
    else:
        parser = ArgumentsBuilder(
            'A script for download wallpapers on https://alphacoders.com/.', 'alphacoders-downloader'
        )

        parser.add_argument(
            '-S', action=CommandsHandler().download, description='Download wallpapers.',
            command_usage='-S wallpapers_url -P path'
        )
        parser.add_argument(
            '-V', action=CommandsHandler.get_version, description='Get version infos.', command_usage='-V'
        )
        with HiddenCursor() as _:
            await parser.build()


def start():
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        if hasattr(main_class, 'client_session'):
            if main_class.client_session is not None and main_class.client_session.closed is False:
                asyncio.get_event_loop().run_until_complete(main_class.client_session.close())
        clear_line()
        print('Stop the script...')
        show()
    except Exception as e:
        if hasattr(main_class, 'client_session'):
            if main_class.client_session is not None and main_class.client_session.closed is False:
                asyncio.get_event_loop().run_until_complete(main_class.client_session.close())
        print_error(str(e))
        show()
