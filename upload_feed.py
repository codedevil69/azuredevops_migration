import os
import subprocess
import sys

# Set these variables with your target organization details
target_org_url = 'https://pkgs.dev.azure.com/your-target-organization'
target_pat = 'YOUR_TARGET_PAT'  # You can also use an environment variable or input() to get this securely.
target_feed = 'YOUR_TARGET_FEED_NAME'
target_project = 'YOUR_TARGET_PROJECT'  # Leave blank if the feed is not scoped to a project

# Command template for pushing packages to Azure DevOps using nuget
nuget_push_cmd_template = 'nuget push "{package_path}" -Source "{feed_url}" -ApiKey az -NonInteractive'

# If your feed is scoped to a project, construct the URL accordingly
if target_project:
    feed_url = f'{target_org_url}/{target_project}/_packaging/{target_feed}/nuget/v3/index.json'
else:
    feed_url = f'{target_org_url}/_packaging/{target_feed}/nuget/v3/index.json'

# Walk through the downloaded_packages directory and upload all .nupkg files
for root, dirs, files in os.walk('downloaded_packages'):
    for filename in files:
        if filename.endswith('.nupkg'):
            package_path = os.path.join(root, filename)
            nuget_push_cmd = nuget_push_cmd_template.format(package_path=package_path, feed_url=feed_url)
            
            # Set the environment variable for the PAT
            env = os.environ.copy()
            env['VSS_NUGET_EXTERNAL_FEED_ENDPOINTS'] = f'{{"endpointCredentials": [{{"endpoint":"{feed_url}", "password":"{target_pat}"}}]}}'

            # Execute the command
            result = subprocess.run(nuget_push_cmd, shell=True, env=env)
            if result.returncode != 0:
                print(f"Failed to push {filename}. Error code: {result.returncode}", file=sys.stderr)
            else:
                print(f"Successfully pushed {filename}")

# Note: Depending on your OS and configuration, you may need to adjust the subprocess.run call for correct execution.
