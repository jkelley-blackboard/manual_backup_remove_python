/*
DDA Query to pull Course Backup Cleanup List
Built on top of Heather Crites query
(https://github.com/hcrites-cscc)

Outputs the same fields as the python script 
however, it does set the deleteMe column to Y
by default. This can be changed by the user.

Feel free to also change the creation_date setting
in the where clause. It is set at 365 by default
just as in the python script.

The where clause also includes a commented
out and clause which allows you to specify
a specific date.

If you have any questions feel free to contact me.
terry.patterson@austincc.edu

Run this against the *_cms_doc database/schema
*/

SELECT 
  xyf_urls.full_path as fullPath,
  'Y' as deleteMe,
  to_char(xyf_files.creation_date,'mm/dd/yyyy') as created,
  split_part(xyf_urls.full_path,'/', '4') as courseId,
  xyf_files.file_size as size

FROM xyf_files
  INNER JOIN xyf_urls on xyf_urls.file_id = xyf_files.file_id

WHERE (
  xyf_urls.full_path like '/internal/courses/%/archive/%' 
  OR xyf_urls.full_path like '/internal/orgs/%/archive/%'
  ) AND xyf_files.creation_date < CURRENT_DATE - 365
  -- AND xyf_files.creation_date < to_date('2020-12-31','YYYY-MM-DD')
  
ORDER BY xyf_urls.full_path
