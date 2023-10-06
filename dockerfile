FROM debian:bullseye
RUN apt-get update && apt-get install -y ffmpeg mediainfo mktorrent python3 python3-pip
RUN pip install loguru DateTime lxml cloudscraper requests openpyxl beautifulsoup4 PyYAML doubaninfo progress torf pathlib argparse typing setuptools qbittorrent-api
WORKDIR /app
COPY . .
RUN mkdir -p /atm
RUN mkdir -p /media
RUN chmod a+x a
ENTRYPOINT "/bin/bash -c"

