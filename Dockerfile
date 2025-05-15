# Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt update && apt install -y libpq-dev python3-dev build-essential curl

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run Gunicorn with our configuration
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]