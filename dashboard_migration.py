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
source_headers = config.source_headers
widgets_api_url_source = config.widgets_api_url_source


pat_target = config.pat_target
organization_target = config.organization_target
target_project = config.target_project
group_id_target = config.group_id_target
target_dashboard = config.target_dashboard
dashboard_api_url_target = config.dashboard_api_url_target
target_headers = config.target_headers




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

def update_dashboard(api_url, data, headers):
    try:
        response = requests.put(api_url, data=json.dumps(data), headers=headers)

        # Check the HTTP status code for success
        if response.status_code == 200:
            print("Dashboard update was successful")
        else:
            print(f"Failed to update dashboard. Status code: {response.status_code}")
            print(f"Response content: {response.text}")

        # Optionally, you can return the response for further processing
        return response

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"Network error: {e}")
        return None

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error parsing JSON response: {e}")
        return None

    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None

def update_widgets(widgets_data, target_project, group_id_target, target_dashboard, headers):
    for widget in widgets_data["value"]:
        widget_create_url = f"https://dev.azure.com/{organization_target}/{target_project}/{group_id_target}/_apis/dashboard/dashboards/{target_dashboard}/widgets/{widget['id']}?api-version=7.1-preview.2"
        response = requests.put(widget_create_url, data=json.dumps(widget), headers=headers)

        if response.status_code == 200:
            print(f"Widget '{widget['name']}' was created/updated")
        else:
            print(f"Failed to create/update: {response.text}")
            #print(f"Failed to create/update the widget '{widget['name']}': {response.text}")


# Get source dashboard data
source_dashboard_data = get_dashboard_data(dashboard_api_url_source, source_headers, source_dashboard)

# Get target dashboard data
target_dashboard_data = get_dashboard_data(dashboard_api_url_target, target_headers, target_dashboard)

# Update target dashboard with source data
target_dashboard_data.update(source_dashboard_data)
response = update_dashboard(dashboard_api_url_target, target_dashboard_data, target_headers)
print(response.status_code)
# Get source widgets data
response = requests.get(widgets_api_url_source, headers=source_headers)
widgets_data = json.loads(response.text)

# Update widgets on the target dashboard
#update_widgets(widgets_data, target_project, group_id_target, target_dashboard, target_headers)
