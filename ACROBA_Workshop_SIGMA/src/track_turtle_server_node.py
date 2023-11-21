# Import necessary libraries
import rospy
import actionlib
from ACROBA_Workshop_SIGMA.msg  import TrackTurtleAction, TrackTurtleResult
from geometry_msgs.msg import Twist

class TrackTurtleServer:
    def __init__(self):
        # Initialize the action server
        self.server = actionlib.SimpleActionServer('/turtle2/track_turtle', TrackTurtleAction, self.execute, False)
        self.server.start()

        # Initialize the turtle command publisher
        self.cmd_vel_pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=1)

    def execute(self, goal):
        # Get the ID of the turtle to track
        turtle_id = goal.turtle_id

        # TODO: Implement logic to make turtle2 track turtle1 using Twist commands

        # For example, you might use the /turtle1/pose topic to get the position of turtle1
        # and then calculate the Twist commands to make turtle2 move towards turtle1.

        # Once tracking is complete, set the result and finish the action
        result = TrackTurtleResult()
        result.success = True
        self.server.set_succeeded(result)

if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node('track_turtle_server_node')

    # Create the TrackTurtleServer object
    server = TrackTurtleServer()

    # Spin to keep the script running
    rospy.spin()

