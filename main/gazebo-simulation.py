#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge, CvBridgeError

import subsystems.modeling._tests.test_modeling as test_modeling
import subsystems.tracking._tests.test_tracking as test_tracking
import subsystems.aiming.filter as test_aiming

from main import setup

import _thread

# https://dabit-industries.github.io/turtlebot2-tutorials/14b-OpenCV2_Python.html

bridge = CvBridge()
cv_image = None

def image_callback(img_msg: Image):
	global cv_image
	rospy.loginfo(img_msg.header)

	# Try to convert the ROS Image message to a CV2 Image
	try:
		cv_image = bridge.imgmsg_to_cv2(img_msg)
	except CvBridgeError as e:
		rospy.logerr("CvBridge Error: {0}".format(e))
	
	# cv2.imshow("Robot Sees Dis", cv_image)
	
def give_frame_to_cv():
	global cv_image
	cv2.imshow("Robot Sees Dis", cv_image)
	return cv_image

def main():
	rospy.init_node("aimbots_cv")
	rospy.loginfo("it's simulatorifying time")
	cv2.namedWindow("Robot Sees Dis")

	image_subscriber = rospy.Subscriber("camera/image_raw", Image, image_callback)

	simple_synchronous, synchronous_with_tracker, multiprocessing_with_tracker = setup(
		team_color=0, # red, 1 is blue
		get_frame = give_frame_to_cv,
		modeling=test_modeling,
		tracker=test_tracking,
		aiming=test_aiming,
		live_camera = True,
		kalman_filters = False,
		with_gui = False,
		filter_team_color = True
		# send_output=simulated_send_output, # this should be commented in once we actually add aiming 
	)

	_thread.start_new_thread(simple_synchronous, ())
	
	rospy.spin()

if __name__ == "__main__":
	main()