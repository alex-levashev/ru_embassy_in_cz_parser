FROM --platform=linux/amd64 selenium/standalone-chrome:latest
USER root

# Install system dependencies
RUN apt-get install -y python3 python3-pip

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir \
        selenium==4.10.0 \
        requests \
        pillow \
        pytesseract 

WORKDIR /app
COPY script.py /app/script.py
ENV PYTHONUNBUFFERED=1
CMD ["python3", "-u", "/app/script.py"]
