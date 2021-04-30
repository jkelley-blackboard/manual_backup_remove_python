# manual_backup_remove_python

Jeff Kelley - jeff.kelley@blackboard.com
Provided without explicit or implied support or warranty from me or Blackboard.

This is an unofficial project to provide method(s) to identify and remove manual course backups - i.e. user created course/org archives, exports and IMS Common Cartridge exports from Blackboard Learn.

The project has two parts:

 1. Methods to generate a list of course backups  A) py script that uses WebDAV to generate the csv list and B) sql script that can generate the list

2. A py script to delete the backups using the list

Note that #2 WILL remove files from the content collection, so use it carefully.
Only you can prevent accidental loss of data.

