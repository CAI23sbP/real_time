#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from message_filters import ApproximateTimeSynchronizer ,Subscriber

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

class SET_ENV():
    def __init__(self,ns):
        """
        Default setting
        """

        self.ns = ns
        self.sub_scan = Subscriber(self.ns + "/scan",LaserScan) #-> 360 3.5 
        self.sub_odom = Subscriber(self.ns + "/odom",Odometry)
        subList = [self.sub_scan, self.sub_odom]
        self.ats = ApproximateTimeSynchronizer(subList, queue_size=1, slop=1)
        
        self.agent_action_pub = rospy.Publisher(
            ns+"/cmd_vel", Twist, queue_size=1
        )
        self.number_of_resets = 0
