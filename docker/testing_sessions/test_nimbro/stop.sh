xhost +local:

docker compose -f laptop_nimbro_connection.yaml down --remove-orphans -v
docker network prune -f

xhost -local:
