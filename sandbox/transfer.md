on host:
```
docker exec -it sandbox-omero-1 bash
```

in docker (as omero-server user (user 1000)):
```
cd /opt/omero/server
source venv3/bin/activate
touch a.fake
omero login --server localhost --port 4064 --user root --password omero-root-password
IMAGE=$(omero import a.fake)
omero script upload --official Send_to_iRODS.py
omero script launch /Send_to_iRODS.py IDs=${IMAGE##Image:}
```

on the host ... success:
```
$ docker exec -it -u irods sandbox-irods-catalog-provider-1 ils -l
/tempZone/home/rods:
  rods              0 demoResc        20480 2024-01-12.02:43 & transfer.tar
```
