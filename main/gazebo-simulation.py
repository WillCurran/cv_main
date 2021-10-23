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
	"""
	Called whenever new data is published to camera/image_raw.

	:param img_msg: Image published
	"""

	global cv_image
	rospy.loginfo(img_msg.header)

	# Try to convert the ROS Image message to a CV2 Image
	try:
		cv_image = bridge.imgmsg_to_cv2(img_msg)
	except CvBridgeError as e:
		rospy.logerr("CvBridge Error: {0}".format(e))
	
	
def give_frame_to_cv():
	"""
	Gives a single frame to the CV module
	"""

	global cv_image
	cv2.imshow("Robot Sees Dis", cv_image)
	cv2.waitKey(1)
	return cv_image

def print_frame(frame_number, color_image, boxes_and_confidences: tuple, horizontal_and_vertical_angle: tuple):
	
	print("Frame: {0}".format(frame_number))

def main():

	rospy.init_node("aimbots_cv")
	rospy.loginfo("it's simulatorifying time")
	cv2.namedWindow("Robot Sees Dis")

	image_subscriber = rospy.Subscriber("camera/image_raw", Image, image_callback)
	
	simple_synchronous, synchronous_with_tracker, multiprocessing_with_tracker = setup(
		team_color			= 0, # red, 1 is blue
		get_frame			= give_frame_to_cv,
		on_next_frame 		= print_frame,
		modeling			= test_modeling,
		tracker				= test_tracking,
		aiming				= test_aiming,
		live_camera			= True,
		kalman_filters		= False,
		with_gui 			= False,
		filter_team_color	= True
	)

	# Run simple_synchronous in parallel
	_thread.start_new_thread(simple_synchronous, ())

	try:
		rospy.spin()
	except KeyboardInterrupt:
		rospy.loginfo("shutting down")
		cv2.destroyAllWindows()

if __name__ == "__main__":
	main()