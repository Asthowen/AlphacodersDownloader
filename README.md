<!--suppress HtmlDeprecatedAttribute -->
<div align="center">
    <h1>
      AlphacodersDownloader
    </h1>
    <div>
        <a href="https://www.python.org/">
            <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Written in Python">
        </a>
        <a href="https://github.com/Asthowen/AlphacodersDownloader">
            <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Uses git">
        </a>
        <br>
        <a href="https://github.com/Asthowen/AlphacodersDownloader/blob/main/LICENSE">
            <img src="https://img.shields.io/github/license/Asthowen/AlphacodersDownloader?style=for-the-badge" alt="License">
        </a>
        <a href="https://github.com/Asthowen/AlphacodersDownloader/stargazers">
            <img src="https://img.shields.io/github/stars/Asthowen/AlphacodersDownloader?style=for-the-badge" alt="Stars">
        </a>
        <br>
        <a href="https://pypi.org/project/AlphacodersDownloader/">
            <img src="https://img.shields.io/pypi/v/AlphacodersDownloader?style=for-the-badge" alt="PyPI version">
        </a>
        <a href="https://pypi.org/project/AlphacodersDownloader/">
            <img src="https://img.shields.io/pypi/dd/AlphacodersDownloader?style=for-the-badge" alt="PyPI downloads">
        </a>
        <br>
        <a href="https://aur.archlinux.org/packages/alphacodersdownloader/">
            <img src="https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white" alt="Arch Linux"/>
        </a>
        <a href="https://github.com/Asthowen/AlphacodersDownloader/releases/latest/">
            <img src="https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white" alt="Debian"/>
        </a>
        <a href="https://github.com/Asthowen/AlphacodersDownloader/releases/latest/">
            <img src="https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white" alt="Fedora"/>
        </a>
    </div>
    <h3>
        <strong>A script for download wallpapers on https://alphacoders.com/ written in Python.</strong>
    </h3>
</div>


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
 curl -s https://asthowen.fr/key.gpg | gpg --dearmor | tee /usr/share/keyrings/asthowen.gpg > /dev/null
```

Add the repository in `/etc/apt/sources.list.d/`:
```bash
 echo 'deb [signed-by=/usr/share/keyrings/asthowen.gpg] https://apt.asthowen.fr stable main' >> /etc/apt/sources.list.d/asthowen-packages.list
```

Update repositories and install package:
```bash
apt update && apt install python3-alphacodersdownloader
```

##### With deb file
Download the latest release on: https://github.com/Asthowen/AlphacodersDownloader/releases/latest.

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
yum check-update
```

And install package:
```bash
yum install AlphacodersDownloader 
```

##### With RPM file
Download the latest release on: https://github.com/Asthowen/AlphacodersDownloader/releases/latest.

Install package (replace fileName by the file name):
```bash
yum install fileName
```

### Install with Snap
Start by install Snap (see https://snapcraft.io/docs/installing-snapd).

And then, install the package:
```bash
snap install alphacoders-downloader
```

### Install with PyPI
Install module:
```bash
python3 -m pip install AlphacodersDownloader
```

### Install manually
Clone the repo and switch to folder:
```bash
git clone https://github.com/Asthowen/AlphacodersDownloader.git && cd AlphacodersDownloader/
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
**Currently, due to the use of CloudFlare, it is no longer possible to retrieve wallpapers directly from https://alphacoders.com. 
So you have to go to the page of the wallpaper you want and scroll to the maximum to display all the wallpapers, you can then download the HTML file of the page.**

### With helper
Start the script:
```bash
alphacoders-downloader
```

Enter the path to the previously downloaded HTML file: `./some.html` for example.

Enter download path: `~/downloads/wallpapers/` for example.

If you want change download speed, start by typing **y** and after that, enter a new download speed, it must be in Ko.

### With arguments
#### Arguments list
`-F` The path to the HTML file of the page containing the wallpapers to download, must be associated with the `-P` argument.
<br>
`-P` The path to download wallpapers, must be associated with the `-F` argument.
<br>
`-D` The download speed, it must be in Ko.
<br>
`-H` The help command.
<br>
`-V` Get infos about version.

#### Examples
Download wallpaper in `~/downloads/wallpapers/`:
```bash
alphacoders-downloader -F ./some.html -P "~/downloads/wallpapers/" -D 1024
```

## Dev
**Before committing an update:**
* The code must have a result of 10/10 with pylint, use the command: `pylint --recursive=y alphacoders_downloader/*`
* The code must be cleaned with black, run the command: `black alphacoders_downloader/ && black setup.py && black build/setup_build.py` 

## Author
[<img width="45" src="https://avatars3.githubusercontent.com/u/59535754?s=400&u=48aecdd175dd2dd8867ae063f1973b64d298220b&v=4" alt="Asthowen">](https://github.com/Asthowen)

## License
**[AlphacodersDownloader](https://github.com/Asthowen/AlphacodersDownloader) | [GNU General Public License v3.0](https://github.com/Asthowen/AlphacodersDownloader/blob/main/LICENSE)**