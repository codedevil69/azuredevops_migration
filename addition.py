def get_version_id(package_name, package_version_number, feed_name, org_url, project, pat):
    package_versions_url = f"{org_url}/{project}/_apis/packaging/Feeds/{feed_name}/Packages?packageNameQuery={package_name}&includeAllVersions=true&api-version={api_version}"
    response = requests.get(package_versions_url, auth=('', pat))
    response.raise_for_status()
    packages = response.json()['value']

    # Find the package that matches the package name
    for pkg in packages:
        if pkg['name'] == package_name:
            # Find the version that matches the version number
            for version in pkg['versions']:
                if version['version'] == package_version_number:
                    return version['id']

    return None

# Modify the download_package function to use the version ID
def download_package(package, package_version_number, feed_name, org_url, project, pat):
    version_id = get_version_id(package['name'], package_version_number, feed_name, org_url, project, pat)
    if version_id is None:
        raise Exception(f"Version ID for package {package['name']} with version {package_version_number} not found")

    package_download_url = f"{org_url}/{project}/_apis/packaging/Feeds/{feed_name}/Packages/{package['id']}/Versions/{version_id}/content?api-version={api_version}"
    response = requests.get(package_download_url, auth=('', pat), stream=True)
    response.raise_for_status()

    package_filename = f"{package['name']}.{package_version_number}.nupkg"
    with open(package_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return package_filename
