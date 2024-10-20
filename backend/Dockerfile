FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

COPY . .
CMD ["sh", "-c", "flask db migrate && flask db upgrade && python main.py"]

