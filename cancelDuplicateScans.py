from CheckmarxPythonSDK.CxOne import (
    cancel_scan,
    get_a_list_of_scans,
)

import json

if __name__ == '__main__':

    # Get a list of all scans    
    ast_scans = get_a_list_of_scans(limit=500)

    runningScans = []
    uniqueProjects = []
    projectScans = []
    duplicateScans = []
    projectBranches = []

    for scan in ast_scans.scans:
        if scan.status == "Running" and scan.status == "Queued":
            runningScans.append(scan)

            #Generate List of all projects that have scans running
            if scan.projectId not in uniqueProjects:
                uniqueProjects.append(scan.projectId)

            if scan.initiator == "dependabot":
                duplicateScans.append(scan)

    for project in uniqueProjects:
        projectScans.clear()
        duplicateScans.clear()
        projectBranches.clear()

        for scan in runningScans:
            if scan.projectId == project:
                projectScans.append(scan)
                if scan.branch not in projectBranches:
                    projectBranches.append(scan.branch)

        #create list of scans with the same project and branch    
        for branch in projectBranches:

            for scan in runningScans:
                if scan.projectId == project and scan.branch == branch:
                    duplicateScans.append(scan)
            
            latestScanTime = duplicateScans[0].createdAt
            latestScan = duplicateScans[0]

            if len(duplicateScans) > 1:
                #find the latest scan request
                for scan in duplicateScans:
                    if scan.createdAt > latestScanTime:
                        latestScanTime = scan.createdAt
                        latestScan = scan

                #Cancel all scans that are not the latest request
                for scan in duplicateScans:
                    if scan != latestScan:
                        cancel_scan(scan.id)