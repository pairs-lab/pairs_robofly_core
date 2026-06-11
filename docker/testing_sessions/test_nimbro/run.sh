xhost +local:

docker compose -f laptop_nimbro_connection.yaml up --attach-dependencies

xhost -local:
