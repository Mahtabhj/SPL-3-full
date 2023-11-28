FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*
#RUN apt-get install aws-cli
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install awscli
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Run database migrations
#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate

# Expose port for the application
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
