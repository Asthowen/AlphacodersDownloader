from alphacoders_downloader.util.utils import limit_tasks, clear_line, print_error
from alphacoders_downloader.util.arguments_builder import ArgumentsBuilder
from alphacoders_downloader.util.utils import create_folder_recursively
from alphacoders_downloader.exceptions import WallpapersNotFounds
from alphacoders_downloader.util.cursor import HiddenCursor, show
from alphacoders_downloader.util.progress_bar import ProgressBar
from alphacoders_downloader.util.spinner import Spinner
from bs4 import BeautifulSoup
from typing import Union
import setproctitle
import aiofiles
import asyncio
import aiohttp
import shutil
import sys
import os


class AlphacodersDownloader:
    def __init__(self, url: str, path: str, client_session: aiohttp.ClientSession):
        self.url = url
        self.path = path if path[-1] == os.sep else path + os.sep
        self.client_session = client_session

        self.temp_path = self.path + 'temp' + os.sep
        self.page_char = ''
        self.progress_bar: Union[ProgressBar, None] = None
        self.spinner: Spinner = Spinner()
        self.temp_images_list = []
        self.images_list = []
        self.links_len = 0
        self.links_got = 0
        self.total_size_to_download = 0
        self.total_size_downloaded = 0

    async def fetch_images(self, image_url: str):
        images_link_list_split = image_url.split('/')
        images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
        images_name_file = images_name_file_thumb.split('-')[len(images_name_file_thumb.split('-')) - 1]
        if os.path.isfile(os.path.join(self.path, images_name_file)) is False:
            image_url = image_url.replace(images_name_file_thumb, '') + images_name_file
            async with self.client_session.head(image_url) as r:
                file_size = int(r.headers['Content-Length'])
                self.total_size_to_download += file_size

            self.images_list.append([image_url, images_name_file, file_size])

    async def parse_url(self, url: str):
        async with self.client_session.get(url, cookies={'AlphaCodersView': 'paged'}) as r:
            page = BeautifulSoup(await r.text(), 'html.parser')

        find_images_urls = page.find('div', {'id': 'page_container'}).find_all('div', 'thumb-container-big')

        if find_images_urls is None:
            raise WallpapersNotFounds(url)
        else:
            for link in find_images_urls:
                href = str(link.find('img').get('src'))

                if (href.startswith('https://images') or href.startswith(
                        'https://mfiles')) and href not in self.temp_images_list:
                    self.temp_images_list.append(href)

            self.links_got += 1

        a_element = page.find('div', {'class': 'pagination-simple center'}).find_all('a')
        changed_element = None
        if a_element is not None and a_element:
            for x in a_element:
                if x.text.strip() == 'Next >>':
                    changed_element = x
                    break
        if changed_element is not None:
            url = changed_element.get('href')
            try:
                url_spliced = url.split('&page=')[1]
            except IndexError:
                url_spliced = url.split('?page=')[1]

            await self.parse_url(f'{self.url}{self.page_char}page=' + url_spliced)

    async def download(self, element: list):
        path = os.path.join(self.path, element[1])
        if os.path.isfile(path) is False:
            temp_path = os.path.join(self.temp_path, element[1])
            file_downloaded = 0
            async with self.client_session.get(element[0]) as r:
                try:
                    async with aiofiles.open(temp_path, 'wb') as f:
                        try:
                            async for data in r.content.iter_chunked(1024):
                                await f.write(data)

                                file_downloaded += len(data)
                                self.progress_bar.progress(len(data))
                        except asyncio.TimeoutError:
                            self.progress_bar.progress(element[2] - file_downloaded, True)
                            return self.progress_bar.print_error(f"Download of file: {element[0]} has been timeout.")
                except aiohttp.ClientPayloadError:
                    self.progress_bar.progress(element[2] - file_downloaded, True)
                    return self.progress_bar.print_error(f"Download of file: {element[0]} raise ClientPayloadError.")

                if os.path.isfile(temp_path):
                    shutil.move(temp_path, path)
        else:
            self.progress_bar.progress(element[2], True)

    async def start(self):
        self.spinner.set_text('Recovery of the URLS of all the pages...')
        await self.spinner.start()

        create_folder_recursively(self.path)
        create_folder_recursively(self.temp_path)

        self.spinner.set_text('Recovery of the URLS of all the wallpapers...')
        self.page_char = '&' if 'https://mobile.alphacoders.com/' not in self.url else '?'
        await self.parse_url(f'{self.url}{self.page_char}page=1')
        self.spinner.set_text('Recovery of the informations about wallpapers...')
        await limit_tasks(10, *[self.fetch_images(element) for element in self.temp_images_list])
        self.temp_images_list.clear()
        self.spinner.stop()

        self.progress_bar = ProgressBar(self.total_size_to_download, 'Downloading wallpapers', speed=True)
        await limit_tasks(10, *[self.download(element) for element in self.images_list])

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
        async with aiohttp.ClientSession() as client_session:
            await AlphacodersDownloader(wallpapers_url, path_to_download, client_session).start()

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
            async with aiohttp.ClientSession() as client_session:
                await AlphacodersDownloader(url, path, client_session).start()
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
        clear_line()
        print('Stop the script...')
        show()
    except Exception as e:
        print_error(str(e))
        show()
