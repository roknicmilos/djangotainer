##################
### Base image ###
##################

FROM python:3.12 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql-client gettext

COPY --chmod=777    ./scripts/     /app/scripts/

COPY ./requirements     /app/requirements
COPY ./src              /app/src


RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app/src

CMD ["sh", "/app/scripts/entrypoint.sh", "start"]


########################
### Production image ###
########################

FROM base AS production

RUN pip install --no-cache-dir -r /app/requirements/production.txt


#########################
### Development image ###
#########################

FROM base AS development

RUN pip install --no-cache-dir -r /app/requirements/development.txt
