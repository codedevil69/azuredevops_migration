import requests
import json
import base64
from requests.auth import HTTPBasicAuth
import config

pat_source = config.pat_source
organization_source = config.organization_source
source_project = config.source_project
group_id_source = config.group_id_source
source_dashboard = config.source_dashboard
dashboard_api_url_source = config.dashboard_api_url_source
widgets_api_url_source = config.widgets_api_url_source
b64_pat_source = config.b64_pat_source

pat_target = config.pat_target
organization_target = config.organization_target
target_project = config.target_project
group_id_target = config.group_id_target
target_dashboard = config.target_dashboard
dashboard_api_url_target = config.dashboard_api_url_target
b64_pat_target = config.b64_pat_target


source_headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic %s" % b64_pat_source,
    "Cache-Control": "no-cache",
}

target_headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic %s" % b64_pat_target,
    "Cache-Control": "no-cache",
}


def get_dashboard_data(api_url, headers, dashboard):
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        try:
            dashboard_data = json.loads(response.text)
            print(f"Request to {dashboard} was successful")
        except json.JSONDecodeError as e:
            print(f"Error parsing dashboard data: {e}")
            dashboard_data = {}  # Set empty data to prevent issues
    else:
        print(f"Failed to retrieve dashboard data. Status code: {response.status_code}")
        dashboard_data = {}

    return dashboard_data


def create_target_dashboard(source_data):
    # Create a new dashboard in the target project
    payload = {
        "name": source_data["name"],  # Use the name of the source dashboard
        "widgets": source_data["widgets"]  # Copy widgets from source to target
    }

    response = requests.post(dashboard_api_url_target, headers=target_headers, json=payload)
    print(response.text)

    if response.status_code == 200:
        try:
            target_dashboard_data = json.loads(response.text)
            print(f"Target dashboard created successfully")
        except json.JSONDecodeError as e:
            print(f"Error parsing target dashboard data: {e}")
            target_dashboard_data = {}  # Set empty data to prevent issues
    else:
        print(f"Failed to create target dashboard. Status code: {response.status_code}")
        target_dashboard_data = {}

    return target_dashboard_data




# Get source dashboard data
source_dashboard_data = get_dashboard_data(dashboard_api_url_source, source_headers, source_dashboard)

# Create target dashboard with widgets from source
target_dashboard_data = create_target_dashboard(source_dashboard_data)

