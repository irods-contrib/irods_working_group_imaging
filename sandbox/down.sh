#!/bin/bash

# get sudo for later
sudo echo -n

# teardown all compose containers
docker-compose down

# lazily unmount nfsrods
export MYMOUNTDIR=${PWD}/irods_client_nfsrods/nfsrods_mount
sudo umount -l ${MYMOUNTDIR}
