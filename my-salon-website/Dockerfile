FROM python:3.9

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run migrations at container start
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:6006"]

# Expose port
EXPOSE 6006
