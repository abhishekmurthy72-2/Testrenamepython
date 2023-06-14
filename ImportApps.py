from CheckmarxPythonSDK.CxOne import (
    get_a_list_of_applications,
    create_an_application
)
from CheckmarxPythonSDK.CxOne.dto import (
    Application,
    ApplicationInput,
    RuleInput
)

import json
import csv

if __name__ == '__main__':

    #loop through csv
    line=0
    with open("./Apps2Import.csv",'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print("Creating app " + row[0])
            if line > 0:
                #create the application input
                rule = RuleInput(rule_type="project.tag.key-value.exists",value=row[1])
                newApp = ApplicationInput(
                    name= row[0],
                    rules= [rule]
                )
                create_an_application(newApp)
            line+=1
         
