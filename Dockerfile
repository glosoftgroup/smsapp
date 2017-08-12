FROM python:2.7

MAINTAINER kent Marete <maretekent@gmail.com>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./ /usr/src/app

RUN pip install -r requirements/development.txt


EXPOSE 80
EXPOSE 8000
EXPOSE 3000

CMD ./devops/wait-for-it.sh -t 300 db:5432 && ./devops/run.sh