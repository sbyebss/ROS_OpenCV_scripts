#!/usr/bin/env python
import cv2
import message_filters
from sensor_msgs.msg import Image
import roslib
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError


def callback(Segmentation, Scene):
    # cv2.imshow("Overlaid", Segmentation.data)
    # cv2.waitKey(3)
    try:
        cv_segmentation = CvBridge().imgmsg_to_cv2(Segmentation, "bgr8")
        cv_scene = CvBridge().imgmsg_to_cv2(Scene, "bgr8")
    except CvBridgeError as e:
        print(e)

    cv2.addWeighted(cv_segmentation, 0.5, cv_scene, 0.5, 0, cv_scene)

    try:
        image_pub.publish(
            CvBridge().cv2_to_imgmsg(cv_scene, "bgr8"))
    except CvBridgeError as e:
        print(e)


global image_pub
rospy.init_node('overlay_operator', anonymous=True)
image_pub = rospy.Publisher("image_topic_2", Image, queue_size=10)
image_sub1 = message_filters.Subscriber(
    '/airsim_node/Car0/front_center_custom/Segmentation', Image)
image_sub2 = message_filters.Subscriber(
    '/airsim_node/Car0/front_center_custom/Scene', Image)
ts = message_filters.ApproximateTimeSynchronizer(
    [image_sub1, image_sub2], 10, 0.1)
ts.registerCallback(callback)
print "1"
try:
    rospy.spin()
except KeyboardInterrupt:
    print("Shutting down")
