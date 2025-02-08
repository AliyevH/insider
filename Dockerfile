# Use Python as base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy test files and dependencies
COPY requirements.txt .
COPY insider_test.py tests/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Selenium Hub
ENV SELENIUM_HUB="http://selenium-hub:4444/wd/hub"

# CMD ["pytest", "tests", "-vvvv"]
