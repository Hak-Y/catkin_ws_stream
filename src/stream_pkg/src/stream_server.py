#!/usr/bin/env python	
#-*- coding:utf-8 -*-	

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import numpy as np

import socket, cv2, pickle, struct
import imutils

## Socket Setup!!!!!!!!!!!!! 근본적으로 FPS, 크기, resolution 해야함

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
#host_ip = '192.168.10.101' # Enter the Drone IP address
#host_ip = '223.171.137.67' # Enter the Drone IP address LTE
#host_ip = '172.30.38.156'
#host_ip = '192.168.0.2'
host_ip = '192.168.0.2'
print('HOST IP:',host_ip)
port = 9976
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen(1)
print("Listening at",socket_address)

class Nodo(object):
    def __init__(self):
        # Params
        self.image = None
        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(1)
        self.prev_time = rospy.Time.now()

        # Publishers
        # self.pub = rospy.Publisher('imagetimer', Image,queue_size=10)
        # Subscribers
        rospy.Subscriber("/front_camera/color/image_raw",Image,self.callback) # 여기서 해상도, FPS 확인 , down scale 해보고 이를 표로 정리

    def callback(self, msg):
        rospy.loginfo('(callback)Image received...')
        self.image = self.br.imgmsg_to_cv2(msg)
   
    def scale_image(self, image, scale_factor=0.5):
        width = int(image.shape[1] * scale_factor)
        height = int(image.shape[0] * scale_factor)
        return cv2.resize(image, (width, height))    

               
    def start_video_stream(self):
        client_socket, addr = server_socket.accept()
        if client_socket:
            while True:
                image = self.image
                frame = self.scale_image(image, scale_factor=0.5)

                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
               
                # FPS 측정 및 로그 출력
                curr_time = rospy.Time.now()
                time_elapsed = (curr_time - self.prev_time).to_sec()
                fps = 1.0 / time_elapsed
                self.prev_time = curr_time  # 이전 시간 업데이트
                rospy.loginfo("FPS: {:.2f}".format(fps))

                # 해상도 확인 및 로그 출력
                width = frame.shape[1]
                height = frame.shape[0]
                rospy.loginfo("Resolution: {}x{}".format(width, height))
                #cv2.imshow("SERVER",frame)
                key = cv2.waitKey(1) & 0xFF
                rospy.loginfo("Open Socket")
                if key == ord('q'):
                    client_socket.close()
       

            while not rospy.is_shutdown():
                br = CvBridge()
                if self.image is not None:
                    # self.pub.publish(br.cv2_to_imgmsg(self.image))
                    self.loop_rate.sleep()


if __name__ == '__main__':
    rospy.init_node("stream_node", anonymous=True)
    my_node = Nodo()
    # my_node.start()
    my_node.start_video_stream()
