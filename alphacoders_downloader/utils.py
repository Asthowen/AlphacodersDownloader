import asyncio


async def limit_task(number: int, *tasks):
    semaphore = asyncio.Semaphore(number)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


def clear_line():
    print('\033[F', end='')
    print('\033[K', end='')


def print_error(text: str):
    print('\033[91m' + text + '\033[0m')
