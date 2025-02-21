# Używamy oficjalnego obrazu Pythona (wersja 3.8-slim)
FROM python:3.11-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik z wymaganiami i instalujemy zależności
COPY requirements.txt requirements.txt

#RUN  pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --upgrade -r requirements.txt
# Kopiujemy cały projekt do kontenera
COPY . .

# Utworzenie katalogu dla modelu
RUN mkdir -p /app/models

# Model będzie dostępny w /app/models po zamontowaniu volume
ENV MODEL_RTG_PATH=/app/models/pneumonia_classification_model_bal.keras
ENV MODEL_USG_PATH=/app/models/breast_usg_model.keras

# Ustawiamy port, na którym będzie działała aplikacja
EXPOSE 5000

# Polecenie uruchamiające aplikację
CMD ["python", "app.py"]
