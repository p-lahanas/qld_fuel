FROM python:3.11-slim


# Copy ETL script
COPY ./etls/etl.py etl.py
COPY ./etls/settings.py settings.py
COPY ./etls/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint
ENTRYPOINT ["python", "etl.py"]
