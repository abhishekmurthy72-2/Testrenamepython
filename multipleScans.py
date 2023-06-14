from CheckmarxPythonSDK.CxOne import (
    get_a_list_of_projects,
    get_project_id_by_name,
    create_scan,
)
from CheckmarxPythonSDK.CxOne.dto import (
    Project,
    Git,
    ScanConfig,
    ScanInput,
)

import json

if __name__ == '__main__':

    #Get projectId
    projects = ["testWebgoat", "API Test"]

    for project in projects:

        project_id = get_project_id_by_name(project)

        scan_input = ScanInput(
            scan_type="git",
            handler=Git(
                repo_url="https://github.com/WebGoat/WebGoat.git",
                branch="main",
            ),
            project=Project(project_id=project_id),
            configs=[
                ScanConfig("sast", {"incremental": "false", "presetName": "ASA Premium"}),
                ScanConfig("sca"),
                ScanConfig("kics")
            ],
            tags={
                "test": "",
                "scan_tag": "test"
            }
        )
        for i in range(1,10):
            scan = create_scan(scan_input=scan_input)

