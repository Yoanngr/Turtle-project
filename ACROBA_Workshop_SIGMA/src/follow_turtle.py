#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class FollowTurtle:
    def __init__(self):
        rospy.init_node('follow_turtle', anonymous=True)

        self.target_turtle_name = "turtle1"  # Name of the turtle to follow
        self.follower_turtle_name = "turtle2"  # Name of the following turtle

        self.target_pose = Pose()
        self.follower_pub = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size=10)
        self.target_sub = rospy.Subscriber("/turtle1/pose", Pose, self.target_pose_callback)

    def target_pose_callback(self, data):
        self.target_pose = data

    def follow(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            # Calculate control commands to make the follower turtle follow the target turtle
            twist = Twist()

            # Calculate the angle between the follower and target turtles
            angle_to_target = self.calculate_angle_to_target()

            # Proportional control to adjust the angular velocity based on the angle error
            proportional_gain = 2.0  # Adjust as needed
            twist.linear.x = 1.0  # Constant linear velocity
            twist.angular.z = proportional_gain * angle_to_target

            self.follower_pub.publish(twist)
            rate.sleep()

    def calculate_angle_to_target(self):
        # Calculate the angle between the follower and target turtles
        angle_to_target = self.target_pose.theta - self.target_pose.theta
        return angle_to_target

if __name__== '__main__':
    try:
        follower = FollowTurtle()
        follower.follow()
    except rospy.ROSInterruptException:
        pass
