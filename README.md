# Backend PoC systemu do analizy obrazowań medycznych trenowanego na symulowanych danych

## Opis projektu

Ten projekt to Proof-of-Concept (PoC) systemu backendowego stworzonego do analizy obrazowań medycznych przy użyciu danych symulowanych. System został zbudowany przy użyciu frameworka Flask z myślą o przetestowaniu kluczowych funkcjonalności związanych z przetwarzaniem i analizą danych medycznych.

## Główne funkcjonalności

- **Przetwarzanie obrazów medycznych:** Obsługa procesu analizy obrazów na podstawie symulowanych danych wejściowych.
- **API REST:** Udostępnia interfejs umożliwiający komunikację klient-serwer.
- **Skalowalność:** Projekt jest gotowy do dalszego rozszerzania funkcjonalności dla zaawansowanych analiz obrazu.
- **Rapid Prototyping:** Możliwość szybkiego wdrożenia i testowania pomysłów.

## Wymagania systemowe

Aby uruchomić projekt, potrzebujesz:

- Python (zalecana wersja 3.11)
- Flask (framework webowy)
- Docker (opcjonalnie, do uruchamiania aplikacji w kontenerze Docker)
- Inne zależności określone w pliku `requirements.txt`

## Zmienne środowiskowe

W projekcie możesz ustawić następujące zmienne środowiskowe:

1. **`FLASK_ENV`**  
   - **Opis:** Określa środowisko pracy aplikacji Flask (np. `development`, `production`).  
   - **Przykład użycia:**  
     ```bash
     export FLASK_ENV=development
     ```
   - **Domyślna wartość:** `production`

2. **`API_KEY`**  
   - **Opis:** Klucz API używany do uwierzytelnienia w aplikacji.  
   - **Przykład użycia:**  
     ```bash
     export API_KEY=some_secret_api_key
     ```
   - **Domyślna wartość:** Brak – należy go ustawić przed uruchomieniem aplikacji.

   Jeśli korzystasz z Dockera, klucz API możesz umieścić w pliku `.env`, np.:

   ```bash
   API_KEY=some_secret_api_key
   ```

3. **`PORT`**  
   - **Opis:** Port, na którym uruchomiona jest aplikacja Flask.  
   - **Przykład użycia:**  
     ```bash
     export PORT=5000
     ```
   - **Domyślna wartość:** `5000`


4. **`PYTHON_VERSION`**  
   - **Opis:** Określa wersję Pythona wymaganą przez projekt. Używane głównie przy konfiguracji kontenerów lub środowisk wirtualnych.  
   - **Przykład użycia:**  
     ```bash
     export PYTHON_VERSION=3.11
     ```
   - **Domyślna wartość:** `3.11`


5. **`AZURE_STORAGE_CONNECTION_STRING`**  (OPCJONALNY)
   - **Opis:** Łańcuch połączenia do kontenera Azure Blob Storage, używany do przechowywania lub pobierania danych, takich jak duże (> 100 MB) modele ML.  
   - **Przykład użycia:**  
     ```bash
     export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=example;AccountKey=some_key;EndpointSuffix=core.windows.net"
     ```
   - **Domyślna wartość:** Brak – konfiguracja opcjonalna, do pracy z zasobami Azure.


6. **`MODEL_USG_PATH`**  (OPCJONALNY)
   - **Opis:** Ścieżka filesystemowa lub blob wskazująca na lokalizację modelu uczenia maszynowego używanego w analizie obrazowań medycznych.  
   - **Przykład użycia:**  
     ```bash
     export MODEL_USG_PATH=/path/to/usg/model
     ```
   - **Dla Dockera:**  
     Jeśli model jest w kontenerze, powinien być uwzględniony podczas budowy obrazu Dockera; ścieżka powinna być zgodna z systemem plików kontenera.

   - **Domyślna wartość:** `breast_usg_model.keras`


Wszystkie powyższe zmienne środowiskowe można ustawić jako zmienne systemowe lub w pliku `.env`.

---

## Instalacja

### Instalacja lokalna

1. **Klonowanie repozytorium:**

   ```bash
   git clone https://github.com/PioDru/FlaskProject.git
   cd ./FlaskProject
   ```

2. **Instalacja wymaganych zależności:**

   Upewnij się, że masz zainstalowane `pip`, a następnie:

   ```bash
   pip install -r requirements.txt
   ```
3. **Ustaw zmienne środowiskowe:**  
   Przykład dla systemu Linux/Mac (w pliku `.env` lub ręcznie):

   ```bash
   export FLASK_ENV=development
   export API_KEY=<Twój_API_Key>
   ```

   Jeśli używasz Dockera, te zmienne można dodać do pliku `.env`, którego Docker odczyta podczas budowania kontenera.


4. **Uruchom serwer Flask:**

   W katalogu projektu uruchom następujące polecenie:

   ```bash
   flask run
   ```

   Domyślnie aplikacja będzie działać na `http://127.0.0.1:5000/`.

### Instalacja i uruchamianie za pomocą Docker

1. **Budowanie obrazu Docker:**

   Aby utworzyć obraz Dockera z aplikacją, wykonaj polecenie w katalogu zawierającym plik `Dockerfile`:

   ```bash
   docker build -t flask-app .
   ```

   Powyższe polecenie buduje nowy obraz o nazwie `flask-app`.

2. **Uruchomienie kontenera Docker:**

   Po utworzeniu obrazu możesz uruchomić kontener za pomocą polecenia:

   ```bash
   docker run -p 5000:5000 --env-file .env flask-app
   ```

   Aplikacja będzie działać na porcie `5000` i będzie dostępna pod adresem `http://127.0.0.1:5000/`.


## Struktura projektu

- `app/` - Główny katalog aplikacji, zawierający logikę backendu.
- `static/` - Pliki statyczne, takie jak obrazy, style CSS itp.
- `templates/` - Szablony HTML używane przez aplikację Flask.
- `requirements.txt` - Lista zależności projektu.
- `Dockerfile` - Plik konfiguracji Docker umożliwiający budowanie obrazu aplikacji.
- `.env` - Opcjonalny plik określający zmienne środowiskowe, który może być wykorzystywany lokalnie lub w Dockerze.

---

## Endpointy REST API

### **Nagłówek X-API-Key**

Aby korzystać z endpointów REST API, musisz użyć nagłówka `X-API-Key`, który zapewnia uwierzytelnianie. Bez poprawnego klucza API żądania będą odrzucane.

- Przykład użycia z `curl`:

    ```bash
    curl --location 'http://127.0.0.1:5000/predict' \
    --header 'Content-Type: application/octet-stream' \
    --header 'X-API-Key: <Twój_API_Key>' \
    --data-binary '@<Ścieżka_Do_Twojego_Pliku_Obrazu>>'  
    ```

  1. **POST /predict**  
     Analizuje dane wejściowe i zwraca wyniki przetwarzania dla obrazów RTG płuc.

     - **Dane wejściowe:** Binarne
     - **Nagłówki:** `X-API-Key` z poprawnym kluczem
     - **Dane wyjściowe:** JSON z rezultatami analizy 
      ```bash
     {
      "label": "<class>",
      "prediction": 0.2
      }
      ```


2. **POST /predictusg**  
   Analizuje dane wejściowe i zwraca wyniki przetwarzania dla obrazów USG piersi.

   - **Dane wejściowe:** Binarne
   - **Nagłówki:** `X-API-Key` z poprawnym kluczem
   - **Dane wyjściowe:** JSON z rezultatami analizy.
      ```bash
        {
            "confidence": 0.9,
            "predicted_class": "<class>"
        }
      ```
---




