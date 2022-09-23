# iRODS / NFSRODS / OMERO sandbox

This directory allows a user to run 3 services:

1. iRODS
2. NFSRODS
3. OMERO

From this directory, run the following blocks in separate terminals:

```
# stand up iRODS
docker-compose up irods-catalog-provider
```

```
# set up NFSRODS
docker exec -u irods omerorods_irods-catalog-provider_1 iadmin mkuser omero-server rodsuser
docker-compose up irods-client-nfsrods
export NFSRODS_IPADDRESS=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' omerorods_irods-client-nfsrods_1)
export MYMOUNTDIR=${PWD}/irods_client_nfsrods/nfsrods_mount
mkdir -p ${MYMOUNTDIR}
sudo mount ${NFSRODS_IPADDRESS}:/ ${MYMOUNTDIR}
```

```
# stand up OMERO
docker-compose up omero
```

Success was demonstrated by connecting to the OMERO server using the OMERO.insight client, uploading a file, and seeing it appear in the iRODS namespace.

