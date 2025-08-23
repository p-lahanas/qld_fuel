FROM python:3.11-slim

# # Install system deps (psycopg2 requires libpq)
# RUN apt-get update && apt-get install -y \
#     gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# Copy dependencies first
COPY ./etls/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy in Alembic config and migrations
COPY ./alembic.ini .
COPY ./alembic alembic


# Default command is to run migrations
ENTRYPOINT ["alembic", "upgrade", "head"]
