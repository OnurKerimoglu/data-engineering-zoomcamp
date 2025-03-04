## Question 1. Understanding docker first run 

**Q:** Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint 
`bash`.\
**A:** the command we need is:
`docker run -it --entrypoint=bash python3.12.8`

**Q:** What's the version of `pip` in the image?\
**A:** running the container in interactive mode, and issuing: `pip --version` reveals that the pip version of pip is 24.3.1

## Question 2. Understanding Docker networking and docker-compose

**Q:** Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?
**A:** hostname should be `db`, as this is the name of the defined service, and port is `5432`, as this is the 'outward' looking port
Note: it rutns out, the assigned container_name, i.e., `postgres` can also be used

## Adding the zone data:
In the docker-compose.yaml, by adding:
```
networks:
  extnw1:
    name: pg-network
    external: true
```
block, and to each service, adding:
```
networks:
  - extnw1
```
We define both the db and pgadmin containers on the previoussly pg-network block.
Now running: 
```
docker run -it \
--network=pg-network  \
taxi_ingest:v001   \
--user=root   \
--password=root   \
--host=pgdatabase   \
--port=5432   \
--db=ny_taxi   \
--tb=zones   \
--url=${URL}
```
inserts the zones table to the ny_taxi database.

## Question 3. Trip Segmentation Count


