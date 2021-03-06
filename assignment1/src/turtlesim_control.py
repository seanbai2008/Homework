#!/usr/bin/python

# ME495 Embedded System for Robotics
# Assignment 1
# Name: Fan Bai
# Student ID: 2937200

# please check the launch file for the turtlesim, because I have worte my parameter and rosbag code in the launch file
 
import rospy
from std_msgs.msg import String 
from geometry_msgs.msg import Twist
import math 
import time
from turtlesim.srv import TeleportAbsolute


# rostopic pub -r 1 /turtlesim1/turtle1/cmd_vel geometry_msgs/Twist '[2, 0, 0]' '[4, 3, 2]' 


def mover():
    


    rospy.wait_for_service('/turtlesim1/turtle1/teleport_absolute')
    set_position = rospy.ServiceProxy('/turtlesim1/turtle1/teleport_absolute',TeleportAbsolute)
    set_position(5.5,5.5,0)

    pub = rospy.Publisher('/turtlesim1/turtle1/cmd_vel',Twist,queue_size=10)
    rate = rospy.Rate(100)

    t0 = time.time()

    T = rospy.get_param('/turtlesim1/T')

    while not rospy.is_shutdown():

        # here I set the period of the function equal to 10sec

        w = 2*math.pi/T

        t = time.time() - t0

        x = math.sin(2*w*t)

        y = math.sin(w*t)

        dx = 2*w*math.cos(2*w*t)
        
        dy = w*math.cos(w*t)

        ddx = -4*w*w*math.sin(2*w*t)

        ddy = - w*w*math.sin(w*t)        
        
        #Here I tried to derive the function of "w" and get d(w) by using Mathematica. However the result is
        #not very promising as the turtle will not return to the origin after finishing one turn, it may because my function is still wrong  

        # angular = (-w*(1/math.cos(2*w*t))*(math.sin(w*t))+2*w*math.cos(t*w)*(1/math.cos(2*t*w))*math.tan(2*t*w))/(1+math.cos(w*t)*math.cos(w*t)*(1/math.cos(2*w*t)*1/math.cos(2*w*t))) 

        angular = (dx*ddy - dy*ddx)/(dx*dx+dy*dy)

        vel = math.sqrt(dx*dx+dy*dy)

        print angular
        
        twist = Twist()

        twist.linear.x = vel # move forward at 0.1 m/s

        twist.linear.y = 0
        
        twist.linear.z = 0

        twist.angular.x = 0

        twist.angular.y = 0

        twist.angular.z = angular

        pub.publish(twist)   
   
        rate.sleep()     

if __name__ == '__main__':
    try:
        rospy.init_node('control_turtlesim', anonymous=True)
        mover()
        rospy.spin()
    except rospy.ROSInterruptException: pass
