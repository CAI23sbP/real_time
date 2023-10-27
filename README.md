# real_time

This is a real time testing git for a trained model in [cai_nav_tool](https://github.com/CAI23sbP/cai_nav_tool)

## We don't provide your robot , you must clone your robot pkg ##

## How to real env test learning ##

please see detail setting args in `agent_real_time.launch`

rolaunch your robot pkg (lidar, motor)
change move_base's topic which is name `cmd_vel` to `dummy`

`roslaunch real_time_pkg agent_real_time.launch`

go to scripts and 

`python3 real_time.py`
