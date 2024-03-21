FROM python:3.12-slim

WORKDIR /app

# Copy requirements file
COPY requirements/prod.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r prod.txt

# Copy the rest of the application files
COPY . .
