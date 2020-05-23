# 命令行
# 通过网络摄像头获取视频 python start.py
# 通过文件获取视频 python start.py --video input/example_01.mp4 --conf conf.json

# import the necessary packages
from pyimagesearch.tempimage import TempImage
from imutils.video import VideoStream
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings and load the configuration
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	print("[信息] 正在读取网络摄像头...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	print("[信息] 正在读取视频文件...")
	vs = cv2.VideoCapture(args["video"])

# initialize the average frame, last
# saved timestamp, and frame motion counter
avg = None
lastSaved = datetime.datetime.now()
motionCounter = 0

# loop over the frames of the video
while True:
	# grab the current frame and initialize
	# the timestamp and occupied/unoccupied text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	timestamp = datetime.datetime.now()
	text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		print("[成功] 视频采集完毕。")
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the average frame is None, initialize it
	if avg is None:
		print("[信息] 正在启动背景模型...")
		avg = gray.copy().astype("float")
		continue

	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	# threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
		cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < conf["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		# (x, y, w, h) = cv2.boundingRect(c)
		# cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

	# draw the text and timestamp on the frame
	ts = timestamp.strftime("%A %d %B %Y %I %M %S %f %p")
	# cv2.putText(frame, "Status: {}".format(text), (10, 20),
	# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	# 	0.35, (0, 0, 255), 1)

	# check to see if the room is occupied
	if text == "Occupied":
		# check to see if enough time has passed between saves
		if (timestamp - lastSaved).seconds >= conf["min_save_seconds"]:
			# increment the motion counter
			motionCounter += 1

			# check to see if the number of frames with consistent motion is
			# high enough
			if motionCounter >= conf["min_motion_frames"]:
				# write the image to temporary file
				t = TempImage()
				cv2.imwrite(t.path, frame)

				# save the image to local disk and cleanup the temporary image
				print("[保存] {}".format(ts))
				save_path = conf["output_folder"]
				auto_path = args.get("video", None).split("/")[1].split(".")[0] + "/"

				if save_path == "":
					try:
						os.mkdir(auto_path)
					except FileExistsError:
						pass

				else:
					try:
						os.mkdir(save_path)
					except FileExistsError:
						pass

					try:
						os.mkdir(save_path + auto_path)
					except FileExistsError:
						pass

				path = "{save_path}{auto_path}{timestamp}.jpg".format(
						save_path=save_path, auto_path=auto_path, timestamp=ts)
				cv2.imencode('.jpg', frame)[1].tofile(path)
				t.cleanup()

				# update the last saved timestamp and reset the motion
				# counter
				lastSaved = timestamp
				motionCounter = 0

	# otherwise, the room is not occupied
	else:
		motionCounter = 0

	# check to see if the frames should be displayed to screen
	if conf["show_video"]:
		# display the security feed
		cv2.imshow("Video Playback", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			print("[信息] 用户中断进程。")
			break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()