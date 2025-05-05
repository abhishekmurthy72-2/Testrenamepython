from CheckmarxPythonSDK.CxOne import (
    get_a_list_of_applications,
    create_an_application
)
from CheckmarxPythonSDK.CxOne.dto import (
    Application,
    ApplicationInput,
    RuleInput
)

import logging
import csv

if __name__ == '__main__':
    #path to csv file
    csvFile="./Apps2Import.csv"

    #loop through csv
    line=0
    with open(csvFile,'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print("Creating app " + row[0])
            appId=row[1]
            tagRule = "APP ID;"+appId
            if line > 0:
                #create the application input
                rule = RuleInput(rule_type="project.tag.key-value.exists",value=tagRule)
                newTag = {'App ID': appId}
                newApp = ApplicationInput(
                    name= row[0],
                    rules= [rule],
                    tags= newTag
                )

                create_an_application(newApp)
            line+=1
//test change
         
