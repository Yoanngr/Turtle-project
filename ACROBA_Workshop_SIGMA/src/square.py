#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class SquareMovement:
    def __init__(self):
        rospy.init_node('square', anonymous=True)
        self.cmd_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_sub = rospy.Subscriber('/turtle1/pose', Pose, self.pose_callback)
        self.rate = rospy.Rate(1)  # 1 Hz
        self.current_pose = Pose()

    def pose_callback(self, data):
        self.current_pose = data

    def move_turtle(self, linear_speed, angular_speed, duration):
        twist_msg = Twist()
        twist_msg.linear.x = linear_speed
        twist_msg.angular.z = angular_speed
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < duration:
            self.cmd_vel_pub.publish(twist_msg)
            self.rate.sleep()
        # Stop the turtle after the specified duration
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        self.cmd_vel_pub.publish(twist_msg)

    def move_in_square(self, side_length):
        for _ in range(8):
            # Move forward
            self.move_turtle(1.0, 0.0, side_length)
            # Turn 90 degrees
            self.move_turtle(0.0, math.radians(90), 2.0)

if __name__ == '__main__':
    square_mover = SquareMovement()
    square_mover.move_in_square(1.0)  # Adjust the side length as needed

