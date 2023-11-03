import os
import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Replace these variables with your information
personal_access_token = 'YOUR_PAT'
organization_url = 'https://dev.azure.com/YOUR_ORGANIZATION'
source_feed = 'SOURCE_FEED_NAME'
destination_feed = 'DESTINATION_FEED_NAME'
api_version = '6.0-preview.1'

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()
packaging_client = connection.clients.get_packaging_client()

# Helper function to get packages from a feed
def get_feed_packages(feed_name):
    get_package_url = f"{organization_url}/_apis/packaging/Feeds/{feed_name}/packages?api-version={api_version}"
    response = requests.get(get_package_url, auth=('', personal_access_token))
    response.raise_for_status()
    packages = response.json()['value']
    return packages

# Helper function to download a package
def download_package(package, feed_name):
    package_id = package['id']
    package_version = package['versions'][0]['version']
    package_download_url = f"{organization_url}/_apis/packaging/Feeds/{feed_name}/npm/packages/{package_id}/versions/{package_version}/content?api-version={api_version}"
    response = requests.get(package_download_url, auth=('', personal_access_token), stream=True)
    response.raise_for_status()

    package_filename = f"{package_id}-{package_version}.nupkg"
    with open(package_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return package_filename

# Helper function to upload a package
def upload_package(package_filename, feed_name):
    package_upload_url = f"{organization_url}/_apis/packaging/Feeds/{feed_name}/npm/packages?api-version={api_version}"
    headers = {'Content-Type': 'application/octet-stream'}
    with open(package_filename, 'rb') as f:
        response = requests.put(package_upload_url, headers=headers, data=f, auth=('', personal_access_token))
    response.raise_for_status()

# Migrate packages from source feed to destination feed
packages = get_feed_packages(source_feed)

for package in packages:
    package_name = package['name']
    print(f"Downloading {package_name}...")
    package_file = download_package(package, source_feed)

    print(f"Uploading {package_name} to destination feed...")
    upload_package(package_file, destination_feed)

    print(f"{package_name} migration completed.")

    # Remove the package file after uploading
    os.remove(package_file)

print("All packages migrated successfully.")
