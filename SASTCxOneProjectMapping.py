from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
    get_a_list_of_projects,
    get_last_scan_info
)
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
import csv

class projectMatch:
  def __init__(self, projectName, sastId, cxOneId):
    self.projectName = projectName
    self.sastId = sastId
    self.cxOneId = cxOneId

  def __iter__(self):
    return iter([self.projectName, self.sastId, self.cxOneId])


if __name__ == '__main__':
    #get cxOne projects
    cxOneProjects = get_a_list_of_projects().projects
    #get sast projects
    projects_api = ProjectsAPI()
    sastProjects = projects_api.get_all_project_details()

    allMatches=[]

    for cxOneProject in cxOneProjects:
        for sastProject in sastProjects:
            if sastProject.name == cxOneProject.name:
                project_match = projectMatch (projectName=cxOneProject.name, sastId=sastProject.project_id, cxOneId=cxOneProject.id)
                allMatches.append(project_match)
    
    with open("projectsMapping.csv", "w") as stream:
        writer = csv.writer(stream)
        writer.writerows(allMatches)