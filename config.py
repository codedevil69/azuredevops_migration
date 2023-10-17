import base64
import requests

#Directory Information, IDs can be found under ::> https://dev.azure.com/[organization]/[project]/_apis/Dashboard/Dashboards/?api-version=6.1-preview
#The Code after project = group_id


#The Source Directory
#----------------------------------------------------------------
pat_source = ""
organization_source = "" 
source_project = "" 
group_id_source = "" #must be ID
source_dashboard = ""

#The Target Directory
#----------------------------------------------------------------
pat_target = ""
organization_target = "" 
target_project = ""
group_id_target = "" #must be ID
target_dashboard = ""
#----------------------------------------------------------------













userpass_source = "" + ":" + pat_source
b64_pat_source = base64.b64encode(userpass_source.encode()).decode()
userpass_target = "" + ":" + pat_target
b64_pat_target = base64.b64encode(userpass_target.encode()).decode()

dashboard_api_url_source = f"https://dev.azure.com/{organization_source}/{source_project}/{group_id_source}/_apis/Dashboard/Dashboards/{source_dashboard}?api-version=7.1-preview.2"
widgets_api_url_source = f"https://dev.azure.com/{organization_source}/{source_project}/{group_id_source}/_apis/Dashboard/Dashboards/{source_dashboard}/widgets?api-version=7.1-preview.2"
dashboard_api_url_target = f"https://dev.azure.com/{organization_target}/{target_project}/{group_id_target}/_apis/Dashboard/Dashboards/{target_dashboard}?api-version=7.1-preview.2"
widgets_api_url_target = f"https://dev.azure.com/{organization_target}/{target_project}/{group_id_target}/_apis/Dashboard/Dashboards/{target_dashboard}/widgets?api-version=7.1-preview.2"


source_headers = {
    "Content-Type": "application/json",
    "Authorization" : "Basic %s" % b64_pat_source,
    "Cache-Control": "no-cache",
}

target_headers = {
    "Content-Type": "application/json",
    "Authorization" : "Basic %s" % b64_pat_target,
    "Cache-Control": "no-cache",
}