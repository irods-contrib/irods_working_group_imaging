#!/bin/bash

# get sudo for later
sudo echo -n

# standup irods
docker-compose up -d irods-catalog-provider

# prepare irods for omero-server user
export irods_catalog_provider_hostname=$(basename ${PWD})_irods-catalog-provider_1
docker exec -it ${irods_catalog_provider_hostname} apt update
docker exec -it ${irods_catalog_provider_hostname} apt install -y netcat
until docker exec -it ${irods_catalog_provider_hostname} nc -z localhost 1247; do sleep 1; echo -n "."; done
docker exec -u irods ${irods_catalog_provider_hostname} iadmin mkuser omero-server rodsuser

# standup nfsrods
docker-compose up -d irods-client-nfsrods

# wait for nfsrods, get IP
export irods_client_nfsrods_hostname=$(basename ${PWD})_irods-client-nfsrods_1
until nc -z localhost 2049; do sleep 1; echo -n "."; done
export NFSRODS_IPADDRESS=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${irods_client_nfsrods_hostname})

# mount nfsrods
export MYMOUNTDIR=${PWD}/irods_client_nfsrods/nfsrods_mount
mkdir -p ${MYMOUNTDIR}
sudo mount ${NFSRODS_IPADDRESS}:/ ${MYMOUNTDIR}

# standup omero
docker-compose up -d omero
