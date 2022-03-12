import asyncio
import os


async def limit_tasks(number: int, *tasks):
    semaphore = asyncio.Semaphore(number)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


def create_folder_recursively(folder: str):
    if os.path.exists(folder) is False:
        os.makedirs(folder)


def clear_line():
    print('\033[F', end='')
    print('\033[K', end='')


def print_error(text: str):
    print('\033[91m' + text + '\033[0m')
