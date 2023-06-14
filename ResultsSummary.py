from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
    get_a_list_of_projects,
    get_last_scan_info
)

import csv
from datetime import datetime

class passwordResult:
  def __init__(self, projectName, tags, queryName, severity, fileName, language, status, foundAt):
    self.projectName = projectName
    self.tags = tags
    self.queryName = queryName
    self.severity = severity
    self.fileName = fileName
    self.language = language
    self.status = status
    self.foundAt = foundAt
  
  def __iter__(self):
    return iter([self.projectName, self.tags, self.queryName, self.severity, self.fileName, self.language, self.status, self.foundAt])

if __name__ == '__main__':

    #get all projects
    allProjects = get_a_list_of_projects(limit=1000)
    allTargetResults = []
    for project in allProjects.projects:
        lastScanInfo = get_last_scan_info(project_ids=[project.id], limit=1)
        scanInfo= lastScanInfo.get(project.id)

        if scanInfo:
            scanData = get_sast_results_by_scan_id(scan_id=scanInfo.id, limit=5000)
            
            #get results from scan that relate to passwords
            allResults = scanData.get("results")

            for result in allResults:
                #add secrets, keys, truffle hog to list of things to look for
                if "password" in result.queryName.lower() or "secret" in result.queryName.lower() or "key" in result.queryName.lower():
                    targetResult = passwordResult(
                        projectName = project.name,
                        tags = project.tags,
                        queryName = result.queryName,
                        severity = result.severity,
                        fileName = result.nodes[0].fileName,
                        language = result.languageName,
                        status = result.status,
                        foundAt = result.foundAt
                        #add file name
                    )

                    allTargetResults.append(targetResult)
            
        else:
            print("This project has no scans: " + project.name)

        #Create csv file with all results
        currentDate = datetime.now().strftime("%d-%m-%Y")
        fileName = "PasswordFindings_" + currentDate + ".csv"
        csvHeaders = ["projectName", "projectTags", "queryName", "severity", "fileName", "language", "status", "foundAt"]
        with open(fileName, "w") as stream:
            writer = csv.DictWriter(stream, fieldnames=csvHeaders)
            writer.writeheader()
            
            writer = csv.writer(stream)
            writer.writerows(allTargetResults)