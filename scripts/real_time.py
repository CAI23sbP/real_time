#!/usr/bin/env python3

import gym,rospy
import numpy as np
from geometry_msgs.msg import Twist,Pose2D,Point, Quaternion
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import math
import torch
from squaternion import Quaternion as Q
import pedsim_msgs.msg as peds
import tf,os
from visualization_msgs.msg import Marker, MarkerArray
import sys
from std_msgs.msg import Bool
import math 
from env_help import SET_ENV

class REAL_AGENT(gym.Env): 
    def __init__(self, namespace):
        rospy.init_node("REAL_AGENT", anonymous=True)
        self.ns = namespace
        self.ns_prefix = lambda x: os.path.join(self.ns, x)


        self._robot_pose = Pose2D()
        self.goal = Pose2D()
        self.scan = np.ones((1)) 
        self.pose = Point()

        set_env=SET_ENV(self.ns)

        self.ats = set_env.ats
        self.ats.registerCallback(self.get_msg)
        self.is_reset = False 
        self.agent_action_pub = set_env.agent_action_pub
        self.number_of_resets = set_env.number_of_resets
        self.sub_goal = rospy.Subscriber(self.ns_prefix("move_base_simple/goal"),PoseStamped, self.cb_goal)
        self.pub_reset = rospy.Publisher(self.ns_prefix("reset"),Bool,queue_size=1)
        self.distance = 10
        self.get_goal = False

    def cb_goal(self,msg):
        self.get_goal = True
        self.goal = msg.pose.position

    def get_msg(self,scan_msg, odom_msg ):
        self.pose = odom_msg.pose.pose.position
        scan = np.array([scan_msg.ranges])
        scan[np.isnan(scan)] = 10.0

        self.scan = np.array([scan])
        self.goal_distance()

    def goal_distance(self):
        dx = (self.pose.x-self.goal.x)**2
        dy = (self.pose.y-self.goal.y)**2
        self.distance = math.sqrt(dx+dy)
        
    def get_data(self):
        self.is_reset = False
        info = {"done":False,"reason":"None"}
        
        if self.get_goal:
            if self.distance <= 0.5:
                info ={"done":True,"reason":"Goal"}
                self.is_reset = True
            
            if np.min(self.scan) <= 0.3:
                info ={"done":True,"reason":"Collision"}
                self.is_reset = True
        
        self.pub_reset.publish(self.is_reset)

        return info

    def reset(self):
        self.agent_action_pub.publish(Twist())
        self.number_of_resets += 1

if "__main__" ==__name__:
    env = REAL_AGENT('/test_1')
    ob = env.reset()
    while not rospy.is_shutdown():
        info = env.get_data()
        if info["done"]:
            if info["reason"] == "Goal":
                env.reset() #Smooth stop

                rospy.logerr(f"[done_reason]: ROBOT IS IN A GOAL ") 

                rospy.signal_shutdown("Everything is done")

            elif info["reason"] == "Collision":
                env.reset() #Smooth stop
                rospy.logerr(f"[done_reason]: COLLISION ") 

                rospy.signal_shutdown("Everything is done")
