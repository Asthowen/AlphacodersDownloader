from alphacoders_downloader.utils import clear_line


class ProgressBar:
    def __init__(self, total: float, prefix: str):
        self.total = total
        self.prefix = prefix

        self.iteration: float = 0

    def set_progress_bar_parameters(
        self, total: float = None, prefix: str = None, iteration: float = None, progress_at_0: bool = False
    ):
        if total is not None:
            self.total = total
        if prefix is not None:
            self.prefix = prefix
        if iteration is not None:
            self.iteration = iteration
        if progress_at_0:
            self.progress(0)

    def progress(self, iteration: float):
        self.iteration = iteration
        self.__update_progress_bar()

    def __update_progress_bar(self):
        f = int(100 * self.iteration // self.total)
        print(f"{self.prefix} [{'█' * f + ' ' * (100 - f)}] {100 * (self.iteration / float(self.total)):.2f}%",
              end='\r')

        if self.iteration == self.total:
            print()
            clear_line()
