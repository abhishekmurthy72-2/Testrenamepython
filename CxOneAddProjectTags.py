from CheckmarxPythonSDK.CxOne import (
    get_a_list_of_projects,
    update_a_project
)
from CheckmarxPythonSDK.CxOne.dto import (
    ProjectInput,
)

import json

if __name__ == '__main__':

    # Get a list of all projects
    allProjects = get_a_list_of_projects(limit=5000)

    for project in allProjects.projects:
        if project.name == "Webgoat.Test.APP05" or project.name == "containerScanTest.APP01":
            tagValue = project.name[(project.name.rfind(".")+1):len(project.name)]
            newTag = {'AppId':tagValue}
            print(newTag)

            updatedProject = ProjectInput(
                name = project.name,
                groups = project.groups,
                repo_url = project.repoUrl,
                main_branch = project.mainBranch,
                origin = project.origin,
                tags = newTag,
                criticality = project.criticality

            )

            update = update_a_project(project_id= project.id, project_input=updatedProject)