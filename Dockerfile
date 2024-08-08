# Use the official Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary tools and add the Tesseract PPA
RUN apt-get update && \
    apt-get install -y \
    lsb-release \
    wget \
    gnupg \
    build-essential \
    git \
    tk \
    tk-dev \
    python3.11 \
    python3-pip \
    python3-tk \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libicu-dev \
    software-properties-common && \
    add-apt-repository ppa:alex-p/tesseract-ocr5 && \
    apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# Verify Tesseract version and available languages
RUN tesseract --version && \
    tesseract --list-langs

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project files into the Docker container
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000
EXPOSE 8765

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8765", "--log-level", "debug", "backend.wsgi:application"]
