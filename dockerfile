FROM debian:bullseye
RUN apt-get update && apt-get install -y ffmpeg mediainfo mktorrent python3 python3-pip git
WORKDIR /app
COPY requirement.txt .
RUN pip install -r requirement.txt
COPY . .
RUN mkdir -p /atm
RUN mkdir -p /media
RUN chmod a+x a
RUN chmod a+x update
ENTRYPOINT "/bin/bash -c"

