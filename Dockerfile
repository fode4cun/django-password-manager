# Pull official base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /futurepassword

# Copy Django project files
COPY . /futurepassword

# Install dependencies
RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --dev --system
