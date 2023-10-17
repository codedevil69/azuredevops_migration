import requests
import json
import config

# Define your Azure DevOps organization URLs and PATs
source_organization_url = f"https://dev.azure.com/{config.organization_source}"
target_organization_url = f"https://dev.azure.com/{config.organization_target}"
source_pat = config.pat_source
target_pat = config.pat_target

# Source and target project names
source_project = config.source_project
target_project = config.target_project

# REST API endpoints for test cases and test suites
source_test_cases_endpoint = f"{source_organization_url}/{source_project}/_apis/test/testcases?api-version=6.0"
target_test_cases_endpoint = f"{target_organization_url}/{target_project}/_apis/test/testcases?api-version=6.0"
source_test_suites_endpoint = f"{source_organization_url}/{source_project}/_apis/test/suites/{source_project}/Test%20Suite?api-version=6.0"
target_test_suites_endpoint = f"{target_organization_url}/{target_project}/_apis/test/suites/{target_project}/Test%20Suite?api-version=6.0"

# Function to create test cases in the target project
def copy_test_cases(test_cases, target_pat, target_test_cases_endpoint):
    headers = {
        "Content-Type": "application/json-patch+json",
        "Authorization": f"Basic {target_pat}"
    }

    for test_case in test_cases:
        test_case["id"] = None  # Remove the ID to create a new test case
        response = requests.post(target_test_cases_endpoint, headers=headers, data=json.dumps([test_case]))
        if response.status_code == 200:
            print(f"Test Case '{test_case['name']}' copied successfully.")
        else:
            print(f"Failed to copy Test Case '{test_case['name']}': {response.text}")

# Function to create a test suite in the target project and add test cases
def copy_test_suite(test_suite, test_cases, target_pat, target_test_suites_endpoint):
    headers = {
        "Content-Type": "application/json-patch+json",
        "Authorization": f"Basic {target_pat}"
    }

    # Create the test suite in the target project
    response = requests.post(target_test_suites_endpoint, headers=headers, data=json.dumps([test_suite]))
    if response.status_code == 200:
        print(f"Test Suite '{test_suite['name']}' created successfully.")
        suite_id = response.json()["id"]
        # Add test cases to the test suite
        add_test_cases_to_suite(suite_id, test_cases, target_pat, target_test_suites_endpoint)
    else:
        print(f"Failed to create Test Suite '{test_suite['name']}': {response.text}")

# Function to add test cases to a test suite
def add_test_cases_to_suite(suite_id, test_cases, target_pat, target_test_suites_endpoint):
    headers = {
        "Content-Type": "application/json-patch+json",
        "Authorization": f"Basic {target_pat}"
    }

    operations = [
        {
            "op": "add",
            "path": "/testcases",
            "value": test_cases
        }
    ]

    response = requests.patch(f"{target_test_suites_endpoint}/{suite_id}", headers=headers, data=json.dumps(operations))
    if response.status_code == 200:
        print(f"Added test cases to Test Suite {suite_id}.")
    else:
        print(f"Failed to add test cases to Test Suite {suite_id}: {response.text}")

# Fetch test cases and test suites from the source project
headers = {
    "Authorization": f"Basic {source_pat}"
}

source_test_cases_response = requests.get(source_test_cases_endpoint, headers=headers)
source_test_suites_response = requests.get(source_test_suites_endpoint, headers=headers)

if source_test_cases_response.status_code == 200 and source_test_suites_response.status_code == 200:
    source_test_cases = source_test_cases_response.json()["value"]
    source_test_suites = source_test_suites_response.json()["value"]
    
    # Copy test cases to the target project
    copy_test_cases(source_test_cases, target_pat, target_test_cases_endpoint)
    
    # Copy test suites to the target project and add test cases
    for source_test_suite in source_test_suites:
        copy_test_suite(source_test_suite, source_test_cases, target_pat, target_test_suites_endpoint)
else:
    print("Failed to fetch test cases or test suites from the source project.")
