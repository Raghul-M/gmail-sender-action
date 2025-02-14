FROM python:3.9-slim

WORKDIR /app

COPY gmail.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/gmail.py"]
