FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# outputs/digests is mounted as a volume at runtime
RUN mkdir -p outputs/digests

CMD ["python", "main.py"]
