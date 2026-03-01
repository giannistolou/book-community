# Build frontend assets
FROM node:20.18 as dependencies

WORKDIR /app
COPY ./package.json .
RUN yarn install --no-cache
COPY ./webpack.common.js .
COPY ./webpack.prod.js .
COPY ./style ./style
COPY ./app.js .
COPY . .
RUN yarn build

# Production Python app
FROM python:3.10.6 as production

# Install Pillow dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app structure and user
RUN mkdir -p /home/app/web/staticfiles /home/app/web/uploadsfiles /home/app/web/database
RUN groupadd -r app && useradd -r -g app -d /home/app/web -m app
RUN chown -R app:app /home/app

# Switch to app user
USER app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# Back to root for pip install
USER root
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
RUN pip install --upgrade pip
COPY --chown=app:app ./requirements.txt .
RUN pip install -r requirements.txt

# Copy frontend build
COPY --from=dependencies --chown=app:app /app/dist ./dist

# Copy project files
COPY --chown=app:app ./public ./public
COPY --chown=app:app . .

# Run as app user
USER app
EXPOSE 8000

CMD ["gunicorn", "bookCommunity.wsgi:application", "--bind", "0.0.0.0:8000"]
