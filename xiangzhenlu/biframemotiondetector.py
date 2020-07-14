# import the necessary packages
import imutils
import cv2

class BiFrameMotionDetector:
	def __init__(self, accumWeight=0.5, deltaThresh=5, minArea=5000):
		# determine the OpenCV version, followed by storing the
		# the frame accumulation weight, the fixed threshold for
		# the delta image, and finally the minimum area required
		# for "motion" to be reported
		self.isv2 = imutils.is_cv2()
		self.accumWeight = accumWeight
		self.deltaThresh = deltaThresh
		self.minArea = minArea

		# initialize the average image for motion detection
		self.lastFrame1 = None

	def update(self, image):
		# initialize the list of locations containing motion
		locs = []

		# 如果前一帧为 None，则将其初始化
		if self.lastFrame1 is None: 
			self.lastFrame1 = image
			return locs

		# 计算当前帧和前一帧的不同 
		frameDelta = cv2.absdiff(self.lastFrame1, image) 
	
		# 当前帧设置为下一帧的前一帧 
		self.lastFrame1 = image.copy() 
	
		# 结果转为灰度图 
		thresh = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY) 
	
		# 图像二值化 
		thresh = cv2.threshold(thresh, self.deltaThresh, 255, cv2.THRESH_BINARY)[1] 

		# find contours in the thresholded image, taking care to
		# use the appropriate version of OpenCV
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# loop over the contours
		for c in cnts:
			# only add the contour to the locations list if it
			# exceeds the minimum area
			if cv2.contourArea(c) > self.minArea:
				locs.append(c)
		
		# return the set of locations
		return locs