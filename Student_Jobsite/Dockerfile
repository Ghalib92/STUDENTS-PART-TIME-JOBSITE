ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "YggpSzdkkw2zkXPSR1FFrWFIBdtM1aB8GUWLNWowXVtCf8bsfM"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

RUN python manage.py collectstatic --noinput


CMD ["gunicorn","--bind",":8000","--workers","2","Student_Jobsite.wsgi"]
