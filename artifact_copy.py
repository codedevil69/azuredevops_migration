import requests

# Replace these variables with your source and destination organization details
source_pat = 'SOURCE_ORG_PAT'
source_org_url = 'https://dev.azure.com/SOURCE_ORGANIZATION'
source_feed = 'SOURCE_FEED_NAME'

destination_pat = 'DESTINATION_ORG_PAT'
destination_org_url = 'https://dev.azure.com/DESTINATION_ORGANIZATION'
destination_feed = 'DESTINATION_FEED_NAME'

# Common headers for Azure DevOps REST API
headers = {'Content-Type': 'application/octet-stream'}

# API version for Azure DevOps Services
api_version = '6.0-preview.1'

# Helper function to get a list of packages from the source feed
def get_feed_packages(feed_name, org_url, pat):
    get_package_url = f"{org_url}/_apis/packaging/Feeds/{feed_name}/packages?api-version={api_version}"
    response = requests.get(get_package_url, auth=('', pat))
    response.raise_for_status()
    return response.json()['value']

# Helper function to download a package from the source feed
def download_package(package, feed_name, org_url, pat):
    package_id = package['id']
    package_version = package['versions'][0]['version']
    package_download_url = f"{org_url}/_apis/packaging/Feeds/{feed_name}/nuget/packages/{package_id}/versions/{package_version}/content?api-version={api_version}"
    response = requests.get(package_download_url, auth=('', pat), stream=True)
    response.raise_for_status()

    package_filename = f"{package['name']}.{package_version}.nupkg"
    with open(package_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return package_filename

# Helper function to upload a package to the destination feed
def upload_package(package_filename, feed_name, org_url, pat):
    package_upload_url = f"{org_url}/_apis/packaging/Feeds/{feed_name}/nuget/packages?api-version={api_version}"
    with open(package_filename, 'rb') as f:
        response = requests.put(package_upload_url, headers=headers, data=f, auth=('', pat))
    response.raise_for_status()

# Migrate packages from source feed to destination feed
packages = get_feed_packages(source_feed, source_org_url, source_pat)

for package in packages:
    package_name = package['name']
    print(f"Downloading {package_name}...")
    package_file = download_package(package, source_feed, source_org_url, source_pat)

    print(f"Uploading {package_name} to destination feed...")
    upload_package(package_file, destination_feed, destination_org_url, destination_pat)

    print(f"{package_name} migration completed.")

    # Remove the package file after uploading
    try:
        os.remove(package_file)
    except OSError as e:
        print(f"Error: {package_file} : {e.strerror}")

print("All packages migrated successfully.")
