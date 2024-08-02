# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Tesseract OCR and dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-tk\
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libicu-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the Docker container
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000
EXPOSE 8765

# Run the Django development server
CMD [ "python","manage.py","runserver","0.0.0.0:8765" ]
# CMD ["gunicorn", "--bind", "0.0.0.0:8765", "backend.wsgi:application"]                
