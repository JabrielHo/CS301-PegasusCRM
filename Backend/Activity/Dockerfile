# Use Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose Flask port
EXPOSE 5004

# Start the app
CMD ["python", "consume.py"]
