#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import socket,cv2, pickle,struct
import time

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_ip = '192.168.50.154' # Here Require CACHE Server IP
# host_ip = '192.168.0.6'
host_ip = '223.171.137.67'
port = 9980
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")

while True:

    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame, send_time = pickle.loads(frame_data, encoding="bytes")

    # Resize the frame to a specific width and height
    frame = cv2.resize(frame, (640,480))

    # Calculate latency and print it on the frame
    receive_time = time.time()
    latency = receive_time - send_time
    latency_text = "Latency: {:.2f} seconds".format(latency)
    cv2.putText(frame, latency_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)   

    cv2.imshow("CLIENT", frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break

client_socket.close()
