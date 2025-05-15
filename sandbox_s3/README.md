# iRODS / S3 / OMERO sandbox

This sandbox uses `docker compose` to run a set of services for iRODS / S3 / OMERO integration testing and development.

## Standup

```
./up.sh
```

This script stands up:

1. iRODS database
2. iRODS catalog service provider
3. iRODS catalog service consumer
4. iRODS S3 API
5. MinIO
6. OMERO database
7. OMERO

The OMERO server requires a few seconds before accepting logins.

## Teardown

```
./down.sh
```

This script brings down all `docker compose` containers.

