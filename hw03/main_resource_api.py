'''MainMenu using the boto3 Resource API'''
import os
import boto3
from botocore.exceptions import NoCredentialsError

# Initialize global variables
s3_resource = boto3.resource('s3')
SELECTED_BUCKET = None

def upload(local_folder_name, bucket_name):
    """Upload files from a local folder to S3, preserving folder structure."""
    if not os.path.isdir(local_folder_name):
        print("Invalid folder path.")
        return

    bucket = s3_resource.Bucket(bucket_name)

    for root, dirs, files in os.walk(local_folder_name):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, local_folder_name)
            try:
                # TODO: 1 - Use the upload file resouce API call

                print(f"Uploaded {file_path} to {bucket_name}/{s3_key}")
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")

def list_contents(bucket_name, server_folder_name):
    """List all files in the given bucket and folder."""
    try:
        bucket = s3_resource.Bucket(bucket_name)
        file_list = []
        for obj in # TODO: 2 - Complete this line using the Resource API
            file_list.append(obj.key)
        if not file_list:
            print("No files found in the specified folder.")
        return file_list
    except Exception as e:
        print(f"Error listing contents: {e}")
        return []

def get_file(bucket_name, server_folder_name, file_name):
    """Retrieve a file object from S3."""
    key = f"{server_folder_name}/{file_name}".strip('/')
    try:
        # TODO: 3 - Use the file resouce API call
        obj = 
        print(f"Retrieved file: {file_name}")
        return obj.get()['Body'].read()
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None

def list_buckets():
    """List all buckets in the AWS account."""
    try:
        # TODO: 4 - Use the file resouce API call
        buckets = 
        if buckets:
            print("\nBuckets available:")
            for idx, bucket in enumerate(buckets, 1):
                print(f"{idx}. {bucket}")       
            choice = int(input("\nSelect a bucket by number: "))
            global SELECTED_BUCKET
            SELECTED_BUCKET = buckets[choice - 1]
            print(f"Selected bucket: {SELECTED_BUCKET}")
        else:
            print("No buckets found.")
    except NoCredentialsError:
        print("AWS credentials not found.")
    except Exception as e:
        print(f"Error listing buckets: {e}")

def backup_files_to_bucket():
    """Backup files from a local folder to the selected S3 bucket."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    folder = input("Enter the local folder path to back up: ")
    upload(folder, SELECTED_BUCKET)

def list_objects_in_bucket():
    """List all objects in the selected S3 bucket."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    server_folder_name = input("Enter the folder name in the bucket (or leave empty for root): ")
    objects = list_contents(SELECTED_BUCKET, server_folder_name)
    if objects:
        print("\nObjects in bucket:")
        for obj in objects:
            print(obj)

def download_object():
    """Download a specific object from the selected S3 bucket."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    server_folder_name = input("Enter the folder name in the bucket (or leave empty for root): ")
    file_name = input("Enter the object key to download: ")
    local_path = input("Enter the local file path to save the object: ")
    try:
        # TODO: 5 - Use the file resouce API call
        file_data = 
        if file_data:
            with open(local_path, 'wb') as file:
                file.write(file_data)
            print(f"Downloaded {file_name} to {local_path}")
    except Exception as e:
        print(f"Error downloading object: {e}")

def generate_presigned_url():
    """Generate a pre-signed URL for the selected object."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    object_key = input("Enter the object key for the pre-signed URL: ")
    try:
        obj = s3_resource.Object(SELECTED_BUCKET, object_key)
        # TODO: 6 - Use the file resouce API call
        url = 
        print(f"Pre-signed URL: {url}")
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")

def list_object_versions():
    """List all version information for the selected object in the bucket."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    object_key = input("Enter the object key to list versions: ")
    try:
        bucket = s3_resource.Bucket(SELECTED_BUCKET)
        # TODO: 7 - Use the file resouce API call
        versions = 
        print(f"\nVersions for {object_key}:")
        for version in versions:
            print(f"VersionId: {version.id}, LastModified: {version.last_modified},"
                  f"Size: {version.size}")
    except Exception as e:
        print(f"Error listing object versions: {e}")

def delete_object():
    """Delete the selected object from the bucket."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    object_key = input("Enter the object key to delete: ")
    try:
        obj = s3_resource.Object(SELECTED_BUCKET, object_key)
        # TODO: 8 - Use the file resouce API call

        print(f"Deleted {object_key} from {SELECTED_BUCKET}")
    except Exception as e:
        print(f"Error deleting object: {e}")

def upload_single_file():
    """Upload a single file to the selected S3 bucket."""
    if not SELECTED_BUCKET:
        print("No bucket selected. Use option 1 to select a bucket.")
        return

    local_file_path = input("Enter the full local file path to upload: ")
    s3_key = input("Enter the S3 key (path and file name) for the file: ")
    try:
        bucket = s3_resource.Bucket(SELECTED_BUCKET)
        # TODO: 9 - Use the file resouce API call

        print(f"Uploaded {local_file_path} to {SELECTED_BUCKET}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def main_menu():
    """Main menu for the application."""
    while True:
        print("\nAWS S3 Manager")
        print("1. List all buckets")
        print("2. Backup files to bucket")
        print("3. List objects in bucket")
        print("4. Download object")
        print("5. Generate pre-signed URL")
        print("6. List object versions")
        print("7. Delete object")
        print("8. Upload a single file")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_buckets()
        elif choice == '2':
            backup_files_to_bucket()
        elif choice == '3':
            list_objects_in_bucket()
        elif choice == '4':
            download_object()
        elif choice == '5':
            generate_presigned_url()
        elif choice == '6':
            list_object_versions()
        elif choice == '7':
            delete_object()
        elif choice == '8':
            upload_single_file()
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
