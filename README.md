<h1 align="center">
  AlphacodersDownloader
</h1>
<p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Written in Python">
    </a>
    <a href="https://github.com/Asthowen/AlphacodersWallpaperDownloader">
        <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Uses git">
    </a>
    <br>
    <a href="https://pypi.org/project/AlphacodersDownloader/">
        <img src="https://img.shields.io/pypi/v/AlphacodersDownloader?style=for-the-badge" alt="PyPI version">
    </a>
    <a href="https://pypi.org/project/AlphacodersDownloader/">
        <img src="https://img.shields.io/pypi/dd/AlphacodersDownloader?style=for-the-badge" alt="PyPI version">
    </a>
    <br>
    <a href="https://github.com/Asthowen/AlphacodersWallpaperDownloader/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Asthowen/AlphacodersWallpaperDownloader?style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/Asthowen/AlphacodersWallpaperDownloader/stargazers">
        <img src="https://img.shields.io/github/stars/Asthowen/AlphacodersWallpaperDownloader?style=for-the-badge" alt="Stars">
    </a>
</p>
<h3 align="center">
    <strong>A script for download backgrounds on https://alphacoders.com/ written in Python.</strong>
</h3>

## Made with
* [**BeautifulSoup4**](https://pypi.org/project/bs4/)
* [**aiofiles**](https://pypi.org/project/aiofiles/)
* [**aiohttp**](https://pypi.org/project/aiohttp/)

## Installation
### Install on Archlinux
Link: https://aur.archlinux.org/packages/python-alphacodersdownloader/

You can use an AUR package manager as [yay](https://github.com/Jguer/yay) or [pamac](https://gitlab.manjaro.org/applications/pamac/) for example.

Example with yay:
```sh
yay -S python-alphacodersdownloader
```

### Install on Debian/Ubuntu
##### With my apt repository
Install requirements:
```bash
apt install curl apt-transport-https gnupg2
```

Import GPG key:
```bash
curl https://apt.asthowen.fr/key.gpg | apt-key add -
```

Add the repository in `/etc/apt/sources.list.d/`:
```bash
echo "deb https://apt.asthowen.fr/ stable main" >> /etc/apt/sources.list.d/asthowen-packages.list
```

Update repositories and install package:
```bash
apt update && apt install python3-alphacodersdownloader
```

##### With deb file
Download latest release on: https://github.com/Asthowen/AlphacodersWallpaperDownloader/releases/latest.

Install package (replace fileName by the file name):
```bash
apt install -f ./fileName
```

### Install on Fedora/RedHat/CentOS/AlmaLinux
##### With my RPM repository
Install requirement:
```bash
yum install curl 
```

Add the repository in `/etc/yum.repos.d/`:
```bash
curl https://rpm.asthowen.fr/asthowen.repo > /etc/yum.repos.d/asthowen.repo
```

Update repositories and install package:
```bash
yum check-update && yum install AlphacodersDownloader 
```

##### With RPM file
Download latest release on: https://github.com/Asthowen/AlphacodersWallpaperDownloader/releases/latest.

Install package (replace fileName by the file name):
```bash
yum install fileName
```

### Install with PyPI
Install module:
```bash
python3 -m pip install AlphacodersDownloader
```

Start the script:
```bash
alphacoders-downloader
```

### Install manually
Clone the repo and switch to folder:
```bash
git clone https://github.com/Asthowen/AlphacodersWallpaperDownloader.git && cd AlphacodersWallpaperDownloader/
```

Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Start the script:
```bash
python3 run.py
```

## Use
Enter a link: https://mobile.alphacoders.com/by-sub-category/227264 or https://wall.alphacoders.com/search.php?search=SAO for example.

Enter download path: `~/downloads/backgrounds/` for example.

## Author
[<img width="45" src="https://avatars3.githubusercontent.com/u/59535754?s=400&u=48aecdd175dd2dd8867ae063f1973b64d298220b&v=4" alt="Asthowen">](https://github.com/Asthowen)

## License
**[AlphacodersWallpaperDownloader](https://github.com/Asthowen/AlphacodersWallpaperDownloader) | [GNU v3.0](https://github.com/Asthowen/AlphacodersWallpaperDownloader/blob/main/LICENSE)**