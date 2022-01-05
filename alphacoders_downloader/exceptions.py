class WallpapersNotFounds(Exception):
    def __init__(self, wallpaper: str):
        super().__init__(f"I can't found wallpapers at URL: {wallpaper}!")
