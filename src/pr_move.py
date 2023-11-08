import rospy
import actionlib
import ACROBA_Workshop_SIGMA.msg
from geometry_msgs.msg import Twist, Pose
import random
import math

class Move:
    feedback_ = ACROBA_Workshop_SIGMA.msg.MoveFeedback()
    result_ = ACROBA_Workshop_SIGMA.msg.MoveResult()

    def __init__(self, name):
        self.name = name
        self.vitesse = Twist()
        self._as = actionlib.SimpleActionServer(self.name, ACROBA_Workshop_SIGMA.msg.MoveAction, execute_cb=self.execute_cb, auto_start=False)
        self._as.start()
        rospy.loginfo("Server Ready...")

    def pose_feedback_callback(self, data):
        self.feedback_.position = data
        self._as.publish_feedback(self.feedback_)

    def execute_cb(self, goal):
        velocity_publisher = rospy.Publisher("/" + goal.turtlename + "/cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/" + goal.turtlename + "/pose", Pose, self.pose_feedback_callback)

        current_distance = 0
        t0 = rospy.Time.now().to_sec()
        success = True
        rospy.loginfo("Let's move your robot")

        while current_distance < goal.distance:
            if goal.isForward:
                self.vitesse.linear.x = abs(goal.vitesse)
            else:
                self.vitesse.linear.x = abs(goal.vitesse)

            velocity_publisher.publish(self.vitesse)
            t1 = rospy.Time.now().to_sec()
            current_distance = goal.vitesse * (t1 - t0)

            if current_distance >= goal.distance:
                self.vitesse.linear.x = 0
                velocity_publisher.publish(self.vitesse)

                # Generate a random angle for the rotation (in radians)
                random_angle = random.uniform(0, 2 * math.pi)
                rospy.loginfo("Rotating by %f radians" % random_angle)

                # Calculate the time needed to perform the rotation
                rotation_time = abs(random_angle / goal.vitesse)
                rotation_start_time = rospy.Time.now().to_sec()

                # Rotate the turtle
                while rospy.Time.now().to_sec() - rotation_start_time < rotation_time:
                    if goal.isForward:
                        self.vitesse.angular.z = abs(goal.vitesse)
                    else:
                        self.vitesse.angular.z = -abs(goal.vitesse)
                    velocity_publisher.publish(self.vitesse)

                # Stop the rotation
                self.vitesse.angular.z = 0
                velocity_publisher.publish(self.vitesse)

                goal.isForward = random.choice([True, False])
                rospy.loginfo("Changing direction to forward: %s" % goal.isForward)

                current_distance = 0
                t0 = rospy.Time.now().to_sec()

        if success:
            rospy.loginfo("%s: Succeeded" % self.name)
            self._as.set_succeeded(self.result_)

if __name__ == "__main__":
    rospy.init_node("Move")
    server = Move(rospy.get_name())
    rospy.spin()

