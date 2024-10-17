# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent .pyc files and enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /back

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Run database migrations and start the Django development server
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000"]
