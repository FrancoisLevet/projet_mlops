FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY bulk_index.py bulk_index.py
COPY language_detection_data_s.csv language_detection_data_s.csv

# Le conteneur s'exécute une fois pour ingérer les données, puis s'arrête
CMD ["python", "bulk_index.py"]
