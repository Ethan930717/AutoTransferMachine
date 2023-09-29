import setuptools

with open("AutoTransferMachine/README.md", "r") as fh:

    setuptools.setup(
name="AutoTransferMachine",
version="0.0.5",
author="hudan717",
author_email="dahupt@gmail.com",
description="PT自动转载工具",
url="https://github.com/Ethan930717/AutoTransferMachine",
packages=setuptools.find_packages(),
license='MIT',
install_requires=[
"ffmpeg",
"mediainfo",
"maketorrent",
"loguru",
"pyyaml",
"doubaninfo",
"requests",
"beautifulsoup4",
"lxml",
"cloudscraper",
"qbittorrent-api",
"openpyxl",
"torf",
"typing",
"pathlib",
"progress",
],
)