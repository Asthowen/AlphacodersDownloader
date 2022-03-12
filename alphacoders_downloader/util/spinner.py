from alphacoders_downloader.util.utils import clear_line
import asyncio


class Spinner:
    def __init__(self, text: str = None):
        self.text = text

        self.dots = ('⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏')
        self.task = None

    async def __start_spinner(self):
        is_first_iter = True
        while True:
            for item in self.dots:
                text = '' if self.text is None else self.text
                if is_first_iter:
                    is_first_iter = False
                else:
                    clear_line()
                print('\033[92m' + item + '\033[0m ' + text)
                await asyncio.sleep(0.08)

    async def start(self):
        self.task = asyncio.get_event_loop().create_task(self.__start_spinner())

    def stop(self):
        if self.task is not None:
            self.task.cancel()
            clear_line()

    def set_text(self, new_text: str):
        self.text = new_text
