# Start with Python base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy all files into the container
COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 8050

CMD ["python", "app.py"]
