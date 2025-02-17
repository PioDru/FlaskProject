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

# Ustawiamy port, na którym będzie działała aplikacja
EXPOSE 5000

# Polecenie uruchamiające aplikację
CMD ["python", "app.py"]
