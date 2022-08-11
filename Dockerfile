# pull official base image
FROM node:16.10.0 as dependencies

COPY ./package.json .
RUN yarn install
COPY ./webpack.config.js .
COPY ./style ./style
COPY ./app.js .
RUN yarn build


FROM python:3.10.6-alpine as production

RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app
# set work directory

USER app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/uploadsfiles
USER root

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY --from=dependencies --chown=app:app ./dist ./dist
# copy project
COPY . .

USER app