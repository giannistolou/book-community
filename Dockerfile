# Stage 1: Build assets
FROM node:20.18 as dependencies

WORKDIR /build
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

# Stage 2: Python app
FROM python:3.12-slim

# Install system dependencies FIRST
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*


# Create app user
RUN groupadd -r app && useradd -r -g app app

# Create directories
RUN mkdir -p /home/app/web
WORKDIR /home/app/web
RUN mkdir -p staticfiles uploadsfiles database

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy webpack assets
COPY --from=dependencies --chown=app:app /build/dist ./dist

# Copy project
COPY --chown=app:app . .
COPY ./public ./public

# Set permissions
RUN chown -R app:app /home/app/web

USER app
EXPOSE 8000

CMD ["gunicorn", "bookCommunity.wsgi:application", \
     "--workers=3", \
     "--worker-class=gevent", \
     "--timeout=300", \
     "--bind=0.0.0.0:8000"]
