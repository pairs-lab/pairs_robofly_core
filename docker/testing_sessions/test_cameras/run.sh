xhost +local:

docker compose -f ./laptop_view_camera.yaml up --attach-dependencies

xhost -local:
