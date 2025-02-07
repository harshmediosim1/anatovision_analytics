FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install dependencies
# Upgrade pip and install Python dependencies
# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set Flask environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]