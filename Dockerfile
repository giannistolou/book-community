# Build frontend assets
FROM node:22-alpine AS dependencies

WORKDIR /app
RUN corepack enable
COPY ./package.json ./yarn.lock ./
RUN yarn install --frozen-lockfile --no-cache
COPY . .
RUN yarn build

# Production Python app
FROM python:3.12.15-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/app
ENV APP_HOME=/home/app/web

# Create app structure and user
RUN groupadd -r app && useradd -r -g app -d $APP_HOME -m app \
    && mkdir -p $APP_HOME/staticfiles $APP_HOME/uploadsfiles $APP_HOME/database \
    && chown -R app:app $HOME
WORKDIR $APP_HOME

# Install Python dependencies (all ship as prebuilt wheels, so no compiler is needed)
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /usr/local/bin/uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/opt/venv/bin:$PATH"
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --no-cache

# Copy frontend build
COPY --from=dependencies --chown=app:app /app/dist ./dist

# Copy project files
COPY --chown=app:app . .

# Run as app user
USER app
EXPOSE 8000

CMD ["gunicorn", "bookCommunity.wsgi:application", "--bind", "0.0.0.0:8000"]
