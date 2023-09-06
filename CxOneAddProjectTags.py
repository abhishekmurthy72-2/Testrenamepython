from CheckmarxPythonSDK.CxOne import (
    get_a_list_of_projects,
    update_a_project
)
from CheckmarxPythonSDK.CxOne.dto import (
    ProjectInput,
)

import csv
import logging

if __name__ == '__main__':

    #variables
    csvFile = '/Users/miguelg/Library/CloudStorage/OneDrive-Checkmarx/Cx1/CustomerMigraitons/Humana/apm_application_and_components_CxOne.csv'
    logging.basicConfig(filename="projectTagUpdates.log", level=logging.DEBUG, format='')
    # Get a list of all projects
    allProjects = get_a_list_of_projects(limit=5000)

    with open(csvFile, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            projectKey = row[1]
            applicationTag = row[0]

            for project in allProjects.projects:
                if projectKey in project.name.upper():
                    newTag = {'APP ID':applicationTag, 'AppSVC ID':projectKey}
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
            
            logging.warning("Project with id: " + projectKey + " was not found")