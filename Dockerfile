FROM python:3.10-slim

# Set workdir
WORKDIR /code

# Install system dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
