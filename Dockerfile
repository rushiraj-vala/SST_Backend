# Use the official Ubuntu image from Docker Hub
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Tesseract OCR and dependencies
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
    libtool \
    autoconf \
    automake \
    && rm -rf /var/lib/apt/lists/*

# Clone and build Tesseract OCR
RUN git clone https://github.com/tesseract-ocr/tesseract.git /tesseract \
    && cd /tesseract \
    && git checkout 5.3.3 \
    && ./autogen.sh \
    && ./configure \
    && make \
    && make install \
    && ldconfig

# Set the working directory inside the Docker container
WORKDIR /app

# Update PATH environment variable if necessary
ENV PATH="/user/bin:${PATH}"

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project files into the Docker container
COPY . /app/

# Verify installation and print versions
RUN tesseract --version && \
    python3 -c "import tkinter; print('tkinter is running')" && \
    echo "PATH: $PATH" && \
    echo "Tesseract version:" && \
    tesseract --version

# Expose port 8000 for the Django application
EXPOSE 8000
EXPOSE 8765

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8765", "--log-level", "debug", "backend.wsgi:application"]
