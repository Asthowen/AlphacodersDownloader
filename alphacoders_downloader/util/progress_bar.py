from alphacoders_downloader.util.utils import clear_line
import time
import math
import os


class ProgressBar:
    def __init__(self, total: float, prefix: str, speed: bool = False):
        self.total = total
        self.prefix = prefix
        self.speed = speed

        self.iteration: float = 0
        self.iteration_eta: float = 0
        self.__speed_value = ''
        self.__speed_latest_value = 0
        self.__speed_latest_time = 0
        self.__speed_eta = ''
        self.__can_use_data = 0
        self.is_started = False

        self.__progress_bar_chars = ('▏', '▎', '▍', '▌', '▋', '▊', '▉')

    def set_total(self, total: float):
        self.total = total

    def set_prefix(self, prefix: str):
        self.prefix = prefix

    def set_iteration(self, iteration: float, ignore_speed=False):
        self.iteration = iteration
        if ignore_speed is False:
            self.iteration_eta = iteration

    def append_iteration(self, iteration: float, ignore_speed=False):
        self.iteration += iteration
        if ignore_speed is False:
            self.iteration_eta += iteration

    def set_progress_at_0(self):
        self.progress(0)
        self.__update_progress_bar()

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

    def progress(self, iteration: float, ignore_speed=False):
        if 0 < iteration <= self.total:
            if self.speed and time.time() - self.__speed_latest_time >= 1:
                if self.__can_use_data >= 2:
                    current_eta = self.iteration_eta - self.__speed_latest_value
                    self.__speed_value = ' - ' + self.__parse_size(current_eta) + ' '
                    self.__speed_eta = '| ' + self.__parse_duration(
                        math.trunc(
                            ((self.total - (self.iteration - self.iteration_eta)) - self.iteration_eta) / current_eta
                        )
                    )
                else:
                    self.__can_use_data += 1

                self.__speed_latest_time = time.time()
                self.__speed_latest_value = self.iteration_eta

            self.append_iteration(iteration, ignore_speed)
            self.__update_progress_bar()
            self.is_started = True

    def print_error(self, text: str):
        if self.is_started:
            print()
            clear_line()
        print('\033[91m' + text + '\033[0m')

    def __update_progress_bar(self):
        terminal_size = os.get_terminal_size(0).columns
        place_to_print = terminal_size - len(self.prefix) - 8 - 14 - 14
        percentage = 100 * (self.iteration / float(self.total))
        filled_length = int(place_to_print * self.iteration // self.total)
        additional_progress = self.__progress_bar_chars[
            int(((place_to_print * self.iteration / self.total) % 1) / (1 / 7))
        ]
        progress_chars = '█' * filled_length + additional_progress + ' ' * (place_to_print - filled_length - 1)

        to_print = f"{self.prefix} [{progress_chars}] {percentage:.2f}%{self.__speed_value}{self.__speed_eta}"
        print(f"{to_print}{(terminal_size - len(to_print)) * ' '}", end='\r')

        if self.iteration == self.total:
            print()
            clear_line()
            self.is_started = False

    @staticmethod
    def __parse_size(num):
        for unit in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB'):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}/s"
            num /= 1024.0

    @staticmethod
    def __parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        return f"{f'{days}d' if days > 0 else ''}{f'{hours}h' if hours > 0 else ''}{f'{minutes}m' if minutes > 0 else ''}{f'{seconds}s' if seconds > 0 else ''} "
