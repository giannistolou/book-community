# pull official base image
FROM node:20.18 AS dependencies  

WORKDIR /app
COPY ./package.json .
RUN yarn install --no-cache
COPY ./webpack.common.js .
COPY ./webpack.prod.js .
COPY ./style ./style
COPY ./app.js .
COPY ./fonts ./fonts
COPY ./images ./images
COPY ./script ./script
RUN yarn build
COPY . .

FROM python:3.12-slim AS production  

# Install system dependencies FIRST (add only what requirements.txt needs)
RUN apt-get update && apt-get install -y \
    gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Create app user and ALL directories as root
RUN groupadd -r app && \
    useradd -r -g app -m -d /home/app app && \
    mkdir -p /home/app/web/{staticfiles,uploadsfiles,database} && \
    chown -R app:app /home/app

# Switch to app user
USER app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# Environment variables (fixed syntax)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies as root (for system libs)
USER root
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy with proper ownership
COPY --from=dependencies --chown=app:app /app/dist ./dist
COPY --chown=app:app ./public ./public
COPY --chown=app:app . .
RUN python manage.py collectstatic --noinput --clear && \
    chown -R app:app /home/app/web/staticfiles /home/app/web/uploadsfiles
USER app
EXPOSE 8000

CMD ["gunicorn", "bookCommunity.wsgi:application", "--bind", "0.0.0.0:8000"]
