# Use the official Python image from the Docker Hub
FROM ubuntu:22.04

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# Install Tesseract OCR and dependencies
RUN apt-get update && \
    apt-get install -y \
    lsb-release\
    wget\
    gnupg\
    build-essential \
    tk\
    tk-dev\
    python3.11\
    python3-pip\
    python3-tk\
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libicu-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the Docker container
WORKDIR /app

ENV PATH="/user/bin:${PATH}"

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy the rest of the project files into the Docker container
COPY . /app/

RUN tesseract --version && \
    python3 -c "import tkinter; print('tkinter is running')"

RUN echo "PATH: $PATH" && \
    echo "Tesseract version:" && \
    tesseract --version
# Expose port 8000 for the Django application
EXPOSE 8000
EXPOSE 8765

# Run the Django development server
# CMD [ "python","manage.py","runserver","0.0.0.0:8765" ]
CMD ["gunicorn", "--bind", "0.0.0.0:8765", "backend.wsgi:application"]                
