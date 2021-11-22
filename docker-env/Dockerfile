FROM python:3.8-buster
RUN python -m pip install --upgrade pip && pip install poetry
RUN apt-get update && apt-get install -y cron

WORKDIR /timeseries-extractor
COPY ./ ./
COPY docker-env/extractor-crontab /etc/cron.d/extractor-crontab
RUN chmod +x ./docker-env/extractor.sh

RUN poetry check
RUN poetry install --no-dev --no-root
RUN poetry show

RUN chmod 0644 /etc/cron.d/extractor-crontab &&\
    crontab /etc/cron.d/extractor-crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
