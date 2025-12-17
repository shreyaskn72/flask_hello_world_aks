FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# Gunicorn will import app.py, NOT run the __main__ block
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
