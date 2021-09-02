import setuptools

with open('README.md', 'r', encoding='utf-8', errors='ignore') as f:
    long_description = f.read()

setuptools.setup(
    name='AlphacodersDownloader',
    version='0.1.0',
    author='Asthowen',
    author_email='contact@asthowen.fr',
    maintainer='Asthowen',
    maintainer_email='contact@asthowen.fr',
    license='GNU v3.0',
    description='A script for download backgrounds on https://alphacoders.com written in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Asthowen/AlphacodersWallpaperDownloader',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['alphacoders-downloader = alphacoders_downloader.alphacoders_downloader:start']
    },
    python_requires='>= 3.6',
    include_package_data=True,
    install_requires=['aiohttp', 'aiofiles', 'beautifulsoup4']
)
