import rospy
import actionlib
import ACROBA_Workshop_SIGMA.msg
from geometry_msgs.msg import Twist, Pose, Point
import math

class Follow:
    feedback_ = ACROBA_Workshop_SIGMA.msg.FollowFeedback()
    result_ = ACROBA_Workshop_SIGMA.msg.FollowResult()

    def __init__(self, name, turtle_name, target_turtle_name):
        self.name = name
        self.turtle_name = turtle_name
        self.target_turtle_name = target_turtle_name
        self.vitesse = Twist()
        self._as = actionlib.SimpleActionServer(self.name, ACROBA_Workshop_SIGMA.msg.FollowAction, execute_cb=self.execute_cb, auto_start=False)
        self._as.start()
        self.target_position = Point()  # Position cible
        self.pose_sub = rospy.Subscriber("/" + self.target_turtle_name + "/pose", Pose, self.target_pose_callback)
        rospy.loginfo("Server Ready...")

    def target_pose_callback(self, data):
        # Mettez à jour la position cible à partir de la position de la tortue cible
        self.target_position = data.position

    def pose_feedback_callback(self, data):
        self.feedback_.position = data
        self._as.publish_feedback(self.feedback_)

    def execute_cb(self, goal):
        velocity_publisher = rospy.Publisher("/" + self.turtle_name + "/cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/" + self.turtle_name + "/pose", Pose, self.pose_feedback_callback)

        success = True
        rospy.loginfo("Let's move your robot to a specific position")

        while not rospy.is_shutdown():
            # Calculate the angle to the target position
            angle_to_target = math.atan2(self.target_position.y - self.feedback_.position.y, self.target_position.x - self.feedback_.position.x)

            # Calculate the linear velocity to move towards the target position
            linear_velocity = 0.2  # Adjust as needed
            self.vitesse.linear.x = linear_velocity

            # Calculate the angular velocity to turn towards the target position
            angular_velocity = 1.0  # Adjust as needed
            self.vitesse.angular.z = angular_velocity * (angle_to_target  -self.feedback_.position.theta)

            velocity_publisher.publish(self.vitesse)

            # Check if the goal is reached
            distance_to_target = math.sqrt((self.target_position.x - self.feedback_.position.x) ** 2 + (self.target_position.y - self.feedback_.position.y) ** 2)
            if distance_to_target < 0.1:  # Adjust the tolerance
                rospy.loginfo("Reached the target position.")
                break

        # Stop the turtle
        self.vitesse.linear.x = 0
        self.vitesse.angular.z = 0
        velocity_publisher.publish(self.vitesse)

        if success:
            rospy.loginfo("%s: Succeeded" % self.name)
            self._as.set_succeeded(self.result_)

if __name__ == "__main__":
    rospy.init_node("Follow")

    # Créer une instance de la classe Follow pour la tortue qui suit la position (turtle1)
    server_turtle1 = Follow("Follow_turtle1", "turtle2", "turtle1")

    rospy.spin()

