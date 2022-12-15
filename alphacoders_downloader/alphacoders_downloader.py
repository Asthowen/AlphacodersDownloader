from alphacoders_downloader.util.utils import limit_tasks, clear_line, print_error
from alphacoders_downloader.util.arguments_builder import ArgumentsBuilder
from alphacoders_downloader.util.utils import create_folder_recursively
from alphacoders_downloader.exceptions import WallpapersNotFounds
from alphacoders_downloader.util.cursor import HiddenCursor, show
from alphacoders_downloader.util.progress_bar import ProgressBar
from alphacoders_downloader import __version__, __license__
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
    def __init__(
        self, url: str, path: str, size: int, client_session: aiohttp.ClientSession
    ):
        self.url = url
        self.path = path if path[-1] == os.sep else path + os.sep
        self.size = size
        self.client_session = client_session

        self.temp_path = self.path + "temp" + os.sep
        self.page_char = ""
        self.progress_bar: Union[ProgressBar, None] = None
        self.spinner: Spinner = Spinner()
        self.temp_images_list = []
        self.images_list = []
        self.links_len = 0
        self.links_got = 0
        self.total_size_to_download = 0
        self.total_size_downloaded = 0

    async def fetch_images(self, image_url: str):
        images_link_list_split = image_url.split("/")
        images_name_file_thumb = images_link_list_split[len(images_link_list_split) - 1]
        images_name_file = images_name_file_thumb.split("-")[
            len(images_name_file_thumb.split("-")) - 1
        ]
        if os.path.isfile(os.path.join(self.path, images_name_file)) is False:
            image_url = image_url.replace(images_name_file_thumb, "") + images_name_file
            async with self.client_session.head(image_url) as request:
                file_size = int(request.headers["Content-Length"])
                self.total_size_to_download += file_size

            self.images_list.append([image_url, images_name_file, file_size])

    async def parse_url(self, url: str):
        async with self.client_session.get(
            url, cookies={"AlphaCodersView": "paged"}
        ) as request:
            page = BeautifulSoup(await request.text(), "html.parser")

        find_images_urls = page.find("div", {"id": "page_container"}).find_all(
            "div", "thumb-container-big"
        )

        if find_images_urls is None:
            raise WallpapersNotFounds(url)

        for a_element in find_images_urls:
            href = str(a_element.find("img").get("src"))

            if (
                href.startswith("https://images") or href.startswith("https://mfiles")
            ) and href not in self.temp_images_list:
                self.temp_images_list.append(href)

        self.links_got += 1

        a_elements = page.find("div", {"class": "pagination-simple center"}).find_all(
            "a"
        )
        changed_element = None
        if a_elements is not None and a_elements:
            for a_element in a_elements:
                if a_element.text.strip() == "Next >>":
                    changed_element = a_element
                    break
        if changed_element is not None:
            url = changed_element.get("href")
            try:
                url_spliced = url.split("&page=")[1]
            except IndexError:
                url_spliced = url.split("?page=")[1]

            await self.parse_url(f"{self.url}{self.page_char}page=" + url_spliced)

    async def download(self, element: list):
        path = os.path.join(self.path, element[1])
        if os.path.isfile(path) is False:
            temp_path = os.path.join(self.temp_path, element[1])
            headers = {}
            temp_file_exist = os.path.isfile(temp_path)
            if temp_file_exist:
                file_size = os.stat(temp_path).st_size
                headers["Range"] = f"bytes={file_size}-"
            file_downloaded = 0

            async with self.client_session.get(element[0], headers=headers) as request:
                try:
                    write_mode = "ab" if temp_file_exist else "wb"
                    async with aiofiles.open(temp_path, write_mode) as file:
                        try:
                            async for data in request.content.iter_chunked(
                                int(self.size / 8)
                            ):
                                await file.write(data)

                                file_downloaded += len(data)
                                self.progress_bar.progress(len(data))
                        except asyncio.TimeoutError:
                            self.progress_bar.progress(
                                element[2] - file_downloaded, True
                            )
                            return self.progress_bar.print_error(
                                f"Download of file: {element[0]} has been timeout."
                            )
                except aiohttp.ClientPayloadError:
                    self.progress_bar.progress(element[2] - file_downloaded, True)
                    return self.progress_bar.print_error(
                        f"Download of file: {element[0]} raise ClientPayloadError."
                    )

                if os.path.isfile(temp_path):
                    shutil.move(temp_path, path)
        else:
            self.progress_bar.progress(element[2], True)

    async def start(self):
        self.spinner.set_text("Recovery of the URLS of all the pages...")
        await self.spinner.start()

        create_folder_recursively(self.path)
        create_folder_recursively(self.temp_path)

        self.spinner.set_text("Recovery of the URLS of all the wallpapers...")
        self.page_char = (
            "&" if "https://mobile.alphacoders.com/" not in self.url else "?"
        )
        await self.parse_url(f"{self.url}{self.page_char}page=1")
        self.spinner.set_text("Recovery of the informations about wallpapers...")
        await limit_tasks(
            10, *[self.fetch_images(element) for element in self.temp_images_list]
        )
        self.temp_images_list.clear()
        self.spinner.stop()

        self.progress_bar = ProgressBar(
            self.total_size_to_download, "Downloading wallpapers", speed=True
        )
        await limit_tasks(10, *[self.download(element) for element in self.images_list])

        shutil.rmtree(self.temp_path)
        print("\033[1mCompleted!\033[0m")


class CommandsHandler:
    @staticmethod
    async def download(command_return: dict):
        wallpapers_url = command_return["args"][command_return["args"].index("-S") + 1]
        if "https://" not in wallpapers_url and "alphacoders.com" not in wallpapers_url:
            print_error("This URL isn't correct.")
            sys.exit()
        path_to_download = command_return["args"][
            command_return["args"].index("-P") + 1
        ]
        if os.access(os.path.dirname(path_to_download), os.W_OK) is False:
            print_error("This path isn't correct.")
            sys.exit()

        size = 2048
        if "-D" in command_return["args"]:
            download_index = command_return["args"].index("-D") + 1
            if download_index < len(command_return["args"]):
                converted_size = int(command_return["args"][download_index])
                if (
                    converted_size % 8 == 0
                    and (converted_size / 8) > 0
                    and ((converted_size / 8) % 8) == 0
                ):
                    size = converted_size

        async with aiohttp.ClientSession() as client_session:
            await AlphacodersDownloader(
                wallpapers_url, path_to_download, size, client_session
            ).start()

    @staticmethod
    def get_version(_):
        version_text = f"\033[1mAlphacodersDownloader {__version__}\033[0m\n"
        version_text += (
            "Created by \033[1mAsthowen\033[0m - \033[1mcontact@asthowen.fr\033[0m\n"
        )
        version_text += f"License: \033[1m{__license__}\033[0m"

        print(version_text)


async def main():
    setproctitle.setproctitle("AlphacodersDownloader")

    if len(sys.argv) <= 1:
        url = ""
        while "https://" not in url and "alphacoders.com" not in url:
            url = input(
                "Please enter the download url (e.g. "
                "https://wall.alphacoders.com/search.php?search=sword+art+online). > "
            ).replace(" ", "")
            clear_line()

        path = ""
        while os.access(os.path.dirname(path), os.W_OK) is False:
            path = input(
                "Please enter the folder where the images are saved (e.g. ~/downloads/wallpapers/). > "
            )
            clear_line()

        size = None
        change_size = False
        while size is None:
            if change_size is False:
                change_size_input = input(
                    "Do you want to change the default download limit of 2Mo/s (y/n)? > "
                )
                clear_line()

            if change_size_input.lower() in ("y", "yes") or change_size:
                change_size = True
                new_size_input = input(
                    "Enter the new speed limit (must be in Ko, and be a multiple of 8) > "
                )
                clear_line()
                if new_size_input.isdigit():
                    converted = int(new_size_input)
                    if (
                        converted % 8 == 0
                        and (converted / 8) > 0
                        and ((converted / 8) % 8) == 0
                    ):
                        size = int(new_size_input)
            else:
                size = 2048

        with HiddenCursor() as _:
            async with aiohttp.ClientSession() as client_session:
                await AlphacodersDownloader(url, path, size, client_session).start()
    else:
        parser = ArgumentsBuilder(
            "A script for download wallpapers on https://alphacoders.com/.",
            "alphacoders-downloader",
        )

        parser.add_argument(
            "-S",
            action=CommandsHandler().download,
            description="Download wallpapers.",
            command_usage="-S wallpapers_url -P path -D 1024",
        )
        parser.add_argument(
            "-V",
            action=CommandsHandler.get_version,
            description="Get version infos.",
            command_usage="-V",
        )
        with HiddenCursor() as _:
            await parser.build()


def start():
    # pylint: disable=W0703
    try:
        os.get_terminal_size(0)
        asyncio.get_event_loop().run_until_complete(main())
    except OSError:
        print_error(
            "Your terminal does not support all the features needed for AlphacodersDownloader, please use "
            "another one."
        )
        show()
    except KeyboardInterrupt:
        clear_line()
        print("Stop the script...")
        show()
    except Exception as exception:
        print_error(str(exception))
        show()
