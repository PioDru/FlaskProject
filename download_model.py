from azure.storage.blob import BlobServiceClient
import os

def download_model():
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container_name = "models"
        local_path = '/app/models'

        print(f"Downloading all files from Azure Storage container '{container_name}' to {local_path}...")

        # Utwórz połączenie z blob storage
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client(container_name)

        # Upewnij się, że katalog docelowy istnieje
        os.makedirs(local_path, exist_ok=True)

        # Pobierz listę wszystkich blobów
        blob_list = container_client.list_blobs()

        # Pobierz każdy plik
        for blob in blob_list:
            print(f"Downloading {blob.name}...")
            blob_client = container_client.get_blob_client(blob.name)

            # Utwórz pełną ścieżkę docelową
            destination_file = os.path.join(local_path, blob.name)

            # Upewnij się, że istnieją wszystkie podkatalogi
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)

            # Pobierz plik
            with open(destination_file, "wb") as file:
                data = blob_client.download_blob()
                data.readinto(file)
            print(f"Successfully downloaded {blob.name}")

        print("All files downloaded successfully")
        return True

    except Exception as e:
        print(f"Error downloading files: {str(e)}")
        return False


if __name__ == "__main__":
    download_model()