from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
    get_a_list_of_projects,
    get_last_scan_info,
    get_all_scanners_results_by_scan_id
)

import csv
import pytz
from datetime import datetime
from dateutil import parser


class vulnData:
  def __init__(self, projectName, tags, type, queryName, severity, fileName, line, language, packageName, CVE_Id, status, state, foundAt):
    self.projectName = projectName
    self.tags = tags
    self.type = type
    self.queryName = queryName
    self.severity = severity
    self.fileName = fileName
    self.line = line
    self.language = language
    self.packageName = packageName
    self. CVE_Id = CVE_Id
    self.status = status
    self.state = state
    self.foundAt = foundAt
  
  def __iter__(self):
    return iter([self.projectName, self.tags, self.type, self.queryName, self.severity, self.fileName, self.line, self.language, self.packageName, self.CVE_Id, self.status, self.state, self.foundAt])

if __name__ == '__main__':

    #set the cutoff date
    utc = pytz.UTC
    cutOffDateStr = "2023-08-01"
    cuffOffDate = parser.parse(cutOffDateStr)
    #get all projects
    allProjects = get_a_list_of_projects(limit=1000)
    allTargetResults = []
    for project in allProjects.projects:
        lastScanInfo = get_last_scan_info(project_ids=[project.id], limit=1)
        scanInfo= lastScanInfo.get(project.id)

        if scanInfo:
            scanDate = parser.parse(scanInfo.createdAt)

            if scanDate > utc.localize(cuffOffDate):
                scanData = get_all_scanners_results_by_scan_id(scan_id=scanInfo.id, limit=10000)    
                #get results from scan that relate to passwords
                allResults = scanData.get("results")

                for result in allResults:
                    resultData = result.data

                    #process sast results
                    if result.type == "sast":
                        targetResult = vulnData(
                            projectName = project.name,
                            tags = project.tags,
                            type = result.type,
                            queryName = resultData.get("queryName"),
                            severity = result.severity,
                            fileName = resultData.get("nodes")[0].get("fileName"),
                            line = resultData.get("nodes")[0].get("line"),
                            language = resultData.get("languageName"),
                            packageName = "",
                            CVE_Id = "",
                            status = result.status,
                            state = result.state,
                            foundAt = result.foundAt
                        )
                        
                        allTargetResults.append(targetResult)
                    
                    if result.type == "sca":
                        targetResult = vulnData(
                            projectName = project.name,
                            tags = project.tags,
                            type = result.type,
                            queryName = resultData.get("packageIdentifier"),
                            severity = result.severity,
                            fileName = "",
                            line = "",
                            language = "",
                            packageName = resultData.get("packageIdentifier"),
                            CVE_Id = result.id,
                            status = result.status,
                            state = result.state,
                            foundAt = result.foundAt
                        )
                        
                        allTargetResults.append(targetResult)

                    #process kics results        
                    if result.type == "kics":
                        targetResult = vulnData(
                            projectName = project.name,
                            tags = project.tags,
                            type = result.type,
                            queryName = resultData.get("queryName"),
                            severity = result.severity,
                            fileName = resultData.get("fileName"),
                            line = resultData.get("line"),
                            language = resultData.get("platform"),
                            packageName = "",
                            CVE_Id = "",
                            status = result.status,
                            state = result.state,
                            foundAt = result.foundAt
                        )
                        
                        allTargetResults.append(targetResult)
            
        else:
            print("This project has no scans: " + project.name)

        #Create csv file with all results
        currentDate = datetime.now().strftime("%d-%m-%Y")
        fileName = "AllFindings_" + currentDate + ".csv"
        csvHeaders = ["projectName", "projectTags", "type", "queryName", "severity", "fileName", "line", "language", "packageName", "CVE_Id", "status", "state", "foundAt"]
        with open(fileName, "w") as stream:
            writer = csv.DictWriter(stream, fieldnames=csvHeaders)
            writer.writeheader()
            
            writer = csv.writer(stream)
            writer.writerows(allTargetResults)