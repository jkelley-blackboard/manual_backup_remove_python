"""
REMOVE cousre backups from a csv list
WARNING:  This module will permanenetly delete manual course backups.
Use at your own risk
No warranty or support provided
jeff.kelley@blackboard.com

"""

from webdav3.client import Client  #https://pypi.org/project/webdavclient3/
import csv


#!!! if you set this to True the script WILL remove files!!!
removeFiles = False      

#this is the connection information for your Learn deployment
#you will need to use a System Administrator account
#or an account with explicit read and remove permissions to /internal/courses
options = {
 'webdav_hostname': "https://host.blackboard.com",
 'webdav_root': "/bbcswebdav/",
 'webdav_login':    "admin",
 'webdav_password': "pass",
}

#open the client
client = Client(options)
x = client.list()


#the file should have at least two columns "deleteMe" (Y/N) and "fullPath"
with open("theList.csv") as csvfile:

    #this pushes the file data into a list of dictionaries
    reader = csv.DictReader(csvfile)

    #itterate on each dictionary in the list
    for row in reader:

        #if the backup doesn't exist, say so and move on
        if not client.check(row.get("fullPath")):
            print("Cannot find: " + row.get("fullPath"))
            continue
        
        #determine if the item is marked to be deleted
        if row.get("deleteMe") == "Y":

            #if the flag is True, this will remove the backup
            if removeFiles:
                client.clean(row.get("fullPath"))

            #determine if the backup still exists or not
            if client.check(row.get("fullPath")):
                print("Not deleted: " + row.get("fullPath"))
            else:
                print("Deleted: " + row.get("fullPath"))

        #not marked for deletion
        else:
            print("Skipped: " + row.get("fullPath"))
