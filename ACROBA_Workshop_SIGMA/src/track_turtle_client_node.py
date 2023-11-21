# Import necessary libraries
import rospy
import actionlib
from ACROBA_Workshop_SIGMA.msg import TrackTurtleAction, TrackTurtleGoal

def track_turtle_client(turtle_id):
    # Create a SimpleActionClient
    client = actionlib.SimpleActionClient('/turtle2/track_turtle', TrackTurtleAction)

    # Wait for the action server to come up
    client.wait_for_server()

    # Create a goal
    goal = TrackTurtleGoal()
    goal.turtle_id = turtle_id

    # Send the goal to the action server
    client.send_goal(goal)

    # Wait for the result
    client.wait_for_result()

    # Print the result
    return client.get_result()

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('track_turtle_client_node')

        # Specify the ID of the turtle to track
        turtle_to_track = 1

        # Call the track_turtle_client function
        result = track_turtle_client(turtle_to_track)

        # Print the result
        print("Tracking result:", result.success)

    except rospy.ROSInterruptException:
        print("Program interrupted before completion")

