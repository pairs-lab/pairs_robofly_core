UAV_NAME=$1

export ROS_MASTER_URI=http://$UAV_NAME:11311
export ROS_IP=192.168.12.11
unset ROS_HOSTNAME

sed -i "s/uav[0-9]\+/$UAV_NAME/g" ./camera_test.rviz

rosrun rviz rviz -d ./camera_test.rviz
