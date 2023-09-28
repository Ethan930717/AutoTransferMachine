import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name="AutoTransferMachine-hudan717",
version="0.0.1",
author="hudan717",
author_email="dahupt@gmail.com",
description="PT自动转载工具",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/Ethan930717/AutoTransferMachine",
packages=setuptools.find_packages(),
License='MIT',
setup_requires=[
"wget",
"build-essential",
"libncursesw5-dev",
"libssl-dev",
"libsqlite3-dev",
"tk-dev",
"libgdbm-dev",
"libc6-dev",
"libbz2-dev",
"libffi-dev",
"zlib1g-dev"
],
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
"qbittorrent-api"
"openpyxl"
"torf"
],
)