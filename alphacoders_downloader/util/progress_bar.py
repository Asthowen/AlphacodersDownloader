from alphacoders_downloader.util.utils import clear_line
import os


class ProgressBar:
    def __init__(self, total: float, prefix: str):
        self.total = total
        self.prefix = prefix

        self.iteration: float = 0
        self.is_started = False

        self.__progress_bar_chars = ('▏', '▎', '▍', '▌', '▋', '▊', '▉')

    def set_total(self, total: float):
        self.total = total

    def set_prefix(self, prefix: str):
        self.prefix = prefix

    def set_iteration(self, iteration: float):
        self.iteration = iteration

    def set_progress_at_0(self):
        self.progress(0)

    def set_progress_bar_parameters(
            self, total: float = None, prefix: str = None, iteration: float = None, progress_at_0: bool = False
    ):
        if total is not None:
            self.set_total(total)
        if prefix is not None:
            self.set_prefix(prefix)
        if iteration is not None:
            self.set_iteration(iteration)
        if progress_at_0:
            self.set_progress_at_0()

    def progress(self, iteration: float):
        if 0 < iteration <= self.total:
            self.set_iteration(iteration)
            self.__update_progress_bar()
            self.is_started = True

    def print_error(self, text: str):
        if self.is_started:
            print()
            clear_line()
        print('\033[91m' + text + '\033[0m')

    def __update_progress_bar(self):
        place_to_print = os.get_terminal_size(0).columns - len(self.prefix) - 14
        percentage = 100 * (self.iteration / float(self.total))
        filled_length = int(place_to_print * self.iteration // self.total)
        additional_progress = self.__progress_bar_chars[
            int(((place_to_print * self.iteration / self.total) % 1) / (1 / 7))
        ]
        progress_chars = '█' * filled_length + additional_progress + ' ' * (place_to_print - filled_length - 1)

        print(f"{self.prefix} [{progress_chars}] {percentage:.2f}%", end='\r')

        if self.iteration == self.total:
            print()
            clear_line()
            self.is_started = False
