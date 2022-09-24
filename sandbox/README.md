# iRODS / NFSRODS / OMERO sandbox

This sandbox uses `docker-compose` to run three services on their default ports:

1. iRODS (1247/1248)
2. NFSRODS (2049)
3. OMERO (4063/4064)

Success was demonstrated by connecting to the OMERO server using the OMERO.insight client, uploading a file, and seeing it appear in the iRODS namespace.

## Standup

```
./up.sh
```

This script stands up iRODS, NFSRODS, and OMERO.

The OMERO server requires a few seconds before accepting logins.

## Teardown

```
./down.sh
```

This script brings down any docker-compose containers and unmounts NFSRODS.

