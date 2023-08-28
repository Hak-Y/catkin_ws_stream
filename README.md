# stream2

This is stream src, which is run in competition. (ubuntu 20.04)

In files, 'image_pub.py' is only test for camcorder. What you are actually using is 'stream_client.py and stream_server.py'

First, Turn on stream_server.py in drone which is using ssh.

Second, Verify whether image topic is subscribed or not.

Thrid, Turn on stream_client.py in your computer.

It is also run visual studio code, but if you want to use visual studio code, you must use virtual environment.

Error Analysis

Most errors are due to either not installing modules or Ubuntu versions. you verify your error code, and install module.

Error is continued, Verify your ubuntu version. ubuntu 18.04 is using 'pickle.loads(frame_data)' in 'stream_client.py' but in ubuntu 20.04, it does not work with only frame_data.

You may insert additional code in stream_client.py. Change your command 'pickle.loads(frame_data)' to 'pickle.loads(frame_data, encoding="bytes")'

It is accept your image file to bytes shape.
