# Imports the Google Cloud client library
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The path to your file to upload
    # source_file_name = "local/path/to/file"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # Instantiates a client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

# The name for the new bucket
bucket_name = ""
source_file_name = ""
destination_blob_name = ""
upload_blob(bucket_name, source_file_name, destination_blob_name)