import requests
import os

# Replace these variables with your organization details
org = 'YOUR_ORG'
project = 'YOUR_PROJECT'
feed = 'YOUR_FEED'
pat = 'YOUR_PAT'
api_version = '6.0-preview.1'

# Base URL for Azure DevOps
base_url = f"https://feeds.dev.azure.com/{org}/{project}/_apis/packaging/Feeds/{feed}"

# Create the session
session = requests.Session()
session.auth = ('', pat)

# Set the headers
headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'application/json'
}

def download_package_versions(package):
    package_versions_url = f"{base_url}/packages/{package['id']}/versions?api-version={api_version}"
    versions_response = session.get(package_versions_url, headers=headers)
    versions_response.raise_for_status()
    versions = versions_response.json()['value']

    # Create directory for the package
    package_dir = os.path.join("downloaded_packages", package['name'])
    os.makedirs(package_dir, exist_ok=True)

    for version in versions:
        package_version = version['version']
        download_url = f"{base_url}/packages/{package['id']}/versions/{version['id']}/content?api-version={api_version}"
        download_response = session.get(download_url, stream=True)
        download_response.raise_for_status()

        # Save the package version
        package_filename = os.path.join(package_dir, f"{package_version}.nupkg")
        with open(package_filename, 'wb') as file:
            for chunk in download_response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {package['name']} version {package_version}")

def download_all_packages():
    # Get the list of packages from the feed
    packages_url = f"{base_url}/packages?api-version={api_version}"
    packages_response = session.get(packages_url, headers=headers)
    packages_response.raise_for_status()
    packages = packages_response.json()['value']

    for package in packages:
        download_package_versions(package)

if __name__ == "__main__":
    download_all_packages()
