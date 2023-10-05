FROM python:3.9
RUN apt-get update && apt-get install -y ffmpeg mediainfo mktorrent
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /atm
ENTRYPOINT ["python3", "main.py", "-yp", "/atm/au.yaml"]

