# real_time

This is a real time testing git for a trained model in [cai_nav_tool](https://github.com/CAI23sbP/cai_nav_tool)

## We don't provide your robot , you must clone your robot pkg ##

## How to real env test learning ##

please see detail setting args in `agent_real_time.launch`

rolaunch your robot pkg (lidar, motor)

example pkg (real_test.tar)

`docker load -i real_test.tar`

`nvidia-docker run -it -d --gpus all  --restart unless-stopped -v /dev:/dev -v /run/user/1000:/run/user/1000 -v /tmp/.X11-unix:/tmp/.X11-unix:ro --privileged --net=host --shm-size=256m -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -e XAUTORITY=/tmp/.docker.xauth -e XDG_RUNTIME_DIR=/run/user/1000 --name "cai_robot" cai_robot:v0.0.1 /bin/bash`

` docker exec -it cai_robot /bin/bash`

`xhost +local:docker`

change move_base's topic which is name `cmd_vel` to `dummy`

`roslaunch real_time_pkg agent_real_time.launch`

go to scripts and 

`python3 real_time.py`
