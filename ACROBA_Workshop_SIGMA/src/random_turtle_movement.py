#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# Initialize current_pose with a default value
current_pose = Pose()

def pose_callback(data):
    # Callback function to get the current pose of the turtle
    global current_pose
    current_pose = data

def move_turtle_spiral():
    # Set up a publisher for the Twist messages
    cmd_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # Set up a subscriber to get the current pose of the turtle
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

    # Set the rate at which to publish Twist messages
    rate = rospy.Rate(5)  # 5 Hz

    # Set initial values
    linear_velocity = 0.2
    angular_velocity = 0.2

    while not rospy.is_shutdown():
        # Create a Twist message
        twist_msg = Twist()

        # Update linear and angular velocities to create a spiral pattern
        linear_velocity += 0.01
        angular_velocity += 0.01

        # Limit angular velocity to avoid too fast rotations
        angular_velocity = min(angular_velocity, 1.0)

        # Set the linear and angular velocities
        twist_msg.linear.x = linear_velocity
        twist_msg.angular.z = angular_velocity

        # Publish the Twist message
        cmd_vel_pub.publish(twist_msg)

        # Log the current pose
        rospy.loginfo("Current Pose: x=%.2f, y=%.2f, theta=%.2f",
                      current_pose.x, current_pose.y, current_pose.theta)

        # Sleep to maintain the desired rate
        rate.sleep()

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('random_turtle_movement', anonymous=True)

        # Move the turtle in a spiral pattern
        move_turtle_spiral()

    except rospy.ROSInterruptException:
        pass

