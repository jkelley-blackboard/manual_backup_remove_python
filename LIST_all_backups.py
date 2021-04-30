"""
Generate a list of all manual backups - archives, exports, and CC exports
Note that this is NOT fast like a DB query would be.  Be patient.
No warranty or support provided
jeff.kelley@blackboard.com

"""

from webdav3.client import Client  #https://pypi.org/project/webdavclient3/
from itertools import islice
from datetime import datetime, timedelta
import csv

#the maximum age of any course backup NOT deleted
daysToKeep = 1460

#number of course directories to check
#for testing set to some nominal number eg. 300
#use None to check all courses 
coursesToCheck = None  

#edit this if you only want certain types
prefixes = ('ExportFile_','ArchiveFile_','CommonCartridge_')         

#this is the connection information for your Learn deployment
#you will need to use a System Administrator account
#or an account with explicit read and remove permissions to /internal/courses
options = {
 'webdav_hostname': "https://host.blackboard.com",
 'webdav_root': "/bbcswebdav/",
 'webdav_login':    "admin",
 'webdav_password': "password",
}

#open and instantiate the client
client = Client(options)
#I found that this is requried, but not sure why
x = client.list()

#build a list of ALL courses in /internal
courseList = client.list("internal/courses")


#this is the list of dictionaries one for each backup
theList = []

#for testing only, using islice to limit itterations
for course in islice(courseList, 0, coursesToCheck):          

    #construct full path to archive directory for this course
    arcpath = "internal/courses/" + course + "archive"

    #execute if archive directory exists
    if client.check(arcpath):
        
        #get a list of all backups in the directory
        backups = client.list(arcpath)                        

        #itterate through each backup
        for backup in backups:

            #filter by filename prefix
            if backup.startswith(prefixes):

                #push the file information into a dictionary
                backupInfo = client.info(arcpath + "/" + backup)

                #convert the created string to a date
                createdDateTime = datetime.strptime(backupInfo.get('created'), "%Y-%m-%dT%H:%M:%SZ")

                #determine if the file is old enough to be removed and asign Y/N to deleteMe
                if createdDateTime < datetime.now()- timedelta(days=daysToKeep):
                    deleteMe = 'Y'
                else:
                    deleteMe = 'N'

                #build a dictionary with addtional values:  course Id, full path and deleteMe Y/N
                addInfo = {'courseId': course[:-1], 'fullPath': arcpath + "/" + backup, 'deleteMe': deleteMe}

                #push these addtional values into the backup item's dictionary
                backupInfo.update(addInfo)

                #add the dictionary to the list
                print("Adding to list: " + backupInfo.get('fullPath'))
                theList.append(backupInfo)

#some housekeeping
print("Total number of course directories: " + str(len(courseList)))
print("Total number of backups found: " + str(len(theList)))
                

#dump the list of dictionaries into a CSV
fieldnames = ["fullPath","deleteMe","created","courseId","size"]
with open('theList.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames = fieldnames, extrasaction='ignore')
    dict_writer.writeheader()
    dict_writer.writerows(theList)



                   

                    


