#!/usr/bin/env python

import rospy
import actionlib
from ACROBA_Workshop_SIGMA.msg import TrackTurtleAction, TrackTurtleGoal, TrackTurtleResult

def move_turtle2_track_client():
    # Create an action client for TrackTurtle action
    client = actionlib.SimpleActionClient('/turtle2/track_turtle', TrackTurtleAction)

    # Wait for the action server to come up
    client.wait_for_server()

    # Create a goal message
    goal = TrackTurtleGoal()
    goal.linear_velocity = 0.5  # Set the desired linear velocity
    goal.angular_velocity = 1.0  # Set the desired angular velocity

    # Send the goal to the action server
    client.send_goal(goal)

    # Wait for the action to finish
    client.wait_for_result()

    # Print the result of the action
    result = client.get_result()
    rospy.loginfo("Action Result: %s", result.success)

def main():
    # Initialize the ROS node
    rospy.init_node('turtle2_track_action_client', anonymous=True)

    # Move turtle2 to track turtle1 using action client
    move_turtle2_track_client()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

