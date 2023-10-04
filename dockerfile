
FROM debian:11
RUN apt-get update && apt-get install -y dos2unix python3.9 python3-pip ffmpeg mediainfo mktorrent
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install AutoTransferMachine
COPY /atm/atm /usr/local/bin/
COPY utils /usr/local/lib/python3.9/dist-packages/AutoTransferMachine/
WORKDIR /atm
COPY atm /atm
RUN rm -f /atm/atm /atm/atm_install.sh