# The updater: Docker's command-line tools (to build and restart the app) plus Python.
FROM python:3.13-alpine
RUN apk add --no-cache docker-cli docker-cli-compose docker-cli-buildx tzdata \
 && pip install --no-cache-dir "cryptography>=44,<51"
WORKDIR /updater
COPY updater.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "updater.py"]
