#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import random

def move_turtle1_random():
    # Set up a publisher for the Twist messages for turtle1
    cmd_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # Set the rate at which to publish Twist messages
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        # Create a Twist message
        twist_msg = Twist()

        # Generate random linear and angular velocities
        twist_msg.linear.x = random.uniform(0.0, 1.0)  # Random linear velocity between 0.0 and 1.0
        twist_msg.angular.z = random.uniform(-1.0, 1.0)  # Random angular velocity between -1.0 and 1.0

        # Publish the Twist message
        cmd_vel_pub.publish(twist_msg)

        # Log the random velocities
        rospy.loginfo("Random Velocities: linear=%.2f, angular=%.2f",
                      twist_msg.linear.x, twist_msg.angular.z)

        # Sleep to maintain the desired rate
        rate.sleep()

def main():
    # Initialize the ROS node
    rospy.init_node('turtle1_random_movement', anonymous=True)

    # Move turtle1 with random velocities
    move_turtle1_random()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

