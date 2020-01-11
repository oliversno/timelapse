#!/usr/local/bin/python3

import cv2 as cv
import argparse
import os
import time

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-dir", "--directory", required=False, default='.', help="image directory. default is current directory")
ap.add_argument("-ext", "--extension", required=False, default='png', help="extension name. default is 'png'.")
ap.add_argument("-o", "--output", required=False, default='output.mp4', help="output video file")
ap.add_argument("-t", "--time", required=True, help="")
ap.add_argument("-et", "--ending_time", required=False, default="-1", help="")
args = vars(ap.parse_args())

# Arguments
dir_path = args['directory']
ext = args['extension']
output = args['output']

images = []
for f in os.listdir(dir_path):
    if f.endswith(ext):
        images.append(f)
images.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)))
end_time = os.path.getctime(os.path.join(dir_path, images[-1]))
start_time = os.path.getctime(os.path.join(dir_path, images[0]))
ending_time = int(args['ending_time'])
if end_time < 0:
    end_time = (end_time - start_time)/size(images)
time_diff = end_time - start_time + ending_time

# Determine the width and height from the first image
image_path = os.path.join(dir_path, images[0])
frame = cv.imread(image_path)
cv.imshow('video',frame)
height, width, channels = frame.shape

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out = cv.VideoWriter(output, fourcc, 20.0, (width, height))
cur_image = 0
for timestep in range(int(float(args['time'])*60)-ending_time):
    print(timestep)
    percent = timestep/(float(args['time'])*60-ending_time)
    date = start_time + time_diff*percent
    if date >= os.path.getctime(os.path.join(dir_path, images[cur_image+1])):
        cur_image += 1
    image_path = os.path.join(dir_path, images[cur_image])
    frame = cv.imread(image_path)

    out.write(frame) # Write out frame to video

    cv.imshow('video',frame)
    if (cv.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break
    time.sleep(1)

# Release everything if job is finished
out.release()
cv.destroyAllWindows()

print("The output video is {}".format(output))