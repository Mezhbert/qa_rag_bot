FROM python:3.11-slim
WORKDIR /app
COPY reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt
COPY . .
CMD ["python", "main.py"]