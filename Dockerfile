FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# The exact build shown in Settings > About: docker build --build-arg APP_COMMIT=$(git rev-parse HEAD) .
ARG APP_COMMIT=""
ENV APP_COMMIT=$APP_COMMIT
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Static files are collected at build time; these values are only for this step.
RUN DJANGO_SECRET_KEY=build-only DATABASE_URL=postgres://build/build python manage.py collectstatic --noinput
RUN useradd --create-home app && chown -R app /app
USER app
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3} --timeout ${GUNICORN_TIMEOUT:-180}"]
