#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
from std_msgs.msg import Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time
 
def callback(data):
    global bridge
    cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    lower = np.array([165,100,100])
    upper = np.array([180,255,255]) 
    red = cv2.inRange(hsv, lowerb=lower, upperb=upper)
           	
    ret,thresh=cv2.threshold(red,0,255,cv2.THRESH_BINARY)
    contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    #cv2.imshow('image',thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
           	
    #frame=thresh
           	
    MaxArea=cv2.contourArea(contours[0])
    MaxNum=0
    for index in range(len(contours)):
    	Area=cv2.contourArea(contours[index])
    	if Area>MaxArea:
    		MaxArea=Area
    		MaxNum=index
    cnt=contours[MaxNum]
           	
    x,y,w,h=cv2.boundingRect(cnt)
    cv_img=cv2.rectangle(cv_img,(x,y),(x+w,y+h),(0,0,255),3)
    xy="(%d,%d)"%(x,y)
    cv2.putText(cv_img,xy,(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    
    #cv2.imshow("frame" , cv_img)
    #cv2.waitKey(1)
    
    start = time.time()
    ros_frame = Image()
    header = Header(stamp = rospy.Time.now())
    header.frame_id = "Camera"
    ros_frame.header=header
    ros_frame.width = 1280
    ros_frame.height = 720
    ros_frame.encoding = "bgr8"
    ros_frame.step = 3840
    ros_frame.data = np.array(cv_img).tostring() #图片格式转换
    
    
           	
    image_pub.publish(ros_frame) #发布消息
    end = time.time()  
    print("cost time:", end-start ) # 看一下每一帧的执行时间，从而确定合适的rate
    rate = rospy.Rate(25) # 10hz 

if __name__ == '__main__':
    rospy.init_node('img_process_node', anonymous=True)
    image_pub=rospy.Publisher('topic_fixed', Image, queue_size = 1) #定义话题
    
    bridge = CvBridge()
    rospy.Subscriber('topic_raw', Image, callback)
    rospy.spin()
    
    
    






