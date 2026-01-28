# alternate OMERO storage futures

## variables

**write internal** - yes/no - Ability to write working memory contents out to storage in/under (managed by) the OMERO server.  This exists today.  The format is currently a proprietary format unchanged from the microscope (as determined by bio-formats).  Future work could be a lossless open format, but this may not prove necessary or worth the effort.

**read external** - yes/no - Ability to read a referenced location and load the contents into working memory.  This may include multiple protocols (NFS, S3, etc.) and file formats and any converters to get a particular file format into working memory.  OMERO currently can reference one external location per 'image/dataset', and perhaps this should be expanded to N/many, but this may not prove necessary or worth the effort.

**write external** - yes/no - Ability to write working memory contents out to storage NOT in/under (managed by) the OMERO server.  This may include multiple protocols (NFS, S3, etc.) and file formats.  This format could initially just be a serialized layout of the current working memory, useful only to the current version of OMERO.  As it becomes more generic, these external files can be used/read/converted by other applications.

**copies** - Number of copies of a file/dataset 'managed' by OMERO.  If a file written to external storage is not also referenced by OMERO... then it may not be considered in this count.

## cases

| case | write internal | read external | write external | copies | description | useful |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | no  | no  | no  | 0 | doesn't make sense | no |
| 1 | no  | no  | yes | 1 | export-only | for migration? |
| 2 | no  | yes | no  | 1 | read-only | a safe playground/viewer? |
| 3 | no  | yes | yes | 1 | omero is app-only | YES, the future/goal |
| 4 | yes | no  | no  | 1 | classic, internal only | YES, but fills up local storage|
| 5 | yes | no  | yes | 1 | classic + 'save as' button | YES, marginally more than classic |
| 6 | yes | yes | no  | 1 | classic + external refs | YES - here TODAY |
| 7 | yes | yes | yes | 2 | ALL THE THINGS | YES, can be used/configured to NOT fill up local storage |

## analysis

Cases 0, 1, and 2 don't seem as immediately practical, perhaps later...

A phased upgrade/rollout/development plan may be...

- [6] -> [7] -> [3]

Once OMERO can write to an external iRODS storage location... iRODS could also 'register' that file or a descendent of that file as a reference back into OMERO for future reading.  This full external write/register/read circle would make OMERO appear to be managing the storage, but it would not be.
