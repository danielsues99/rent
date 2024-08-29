FROM python:3.6-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

COPY init_db.sh /app/

RUN chmod +x /app/init_db.sh

EXPOSE 4000

CMD ["/app/init_db.sh"]