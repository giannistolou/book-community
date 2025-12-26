# pull official base image
FROM node:20.18 as dependencies

COPY ./package.json .
RUN yarn install
COPY ./webpack.common.js .
COPY ./webpack.prod.js .
COPY ./style ./style
COPY ./app.js .
COPY ./fonts ./fonts
COPY ./images ./images
COPY ./script ./script
RUN yarn build
COPY . .



FROM python:3.12 as production

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
RUN mkdir $APP_HOME/database
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
COPY ./public ./public
COPY  --chown=app:app . . 


USER app
EXPOSE 8000


CMD ["gunicorn", "bookCommunity.wsgi:application", "--bind", "0.0.0.0:8000"]