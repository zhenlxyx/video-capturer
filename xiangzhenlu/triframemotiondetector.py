# import the necessary packages
import imutils
import cv2

class TriFrameMotionDetector:
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
		self.lastFrame2 = None

	def update(self, image):
		# initialize the list of locations containing motion
		locs = []

		# 如果前二帧为 None，则将其初始化，并计算前两帧的不同
		if self.lastFrame2 is None:
			if self.lastFrame1 is None:
				self.lastFrame1 = image
			else:
				self.lastFrame2 = image
				global frameDelta1  # 全局变量
				frameDelta1 = cv2.absdiff(self.lastFrame1, self.lastFrame2)  # 帧差一
			return locs

		# 计算当前帧和前两帧的不同，计算三帧差分
		frameDelta = cv2.absdiff(self.lastFrame2, image)  # 帧差二
		thresh = cv2.bitwise_and(frameDelta1, frameDelta)  # 图像与运算
		thresh2 = thresh.copy()

		# 当前帧设置为下一帧的前一帧，前一帧设为下一帧的前二帧，帧差二设为帧差一
		self.lastFrame1 = self.lastFrame2
		self.lastFrame2 = image.copy()
		frameDelta1 = frameDelta

		# 结果转为灰度图
		thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

		# 图像二值化
		thresh = cv2.threshold(thresh, self.deltaThresh, 255, cv2.THRESH_BINARY)[1]

		# 去除图像噪声，先腐蚀再膨胀（形态学开运算）
		thresh = cv2.dilate(thresh, None, iterations=3)
		thresh = cv2.erode(thresh, None, iterations=1)

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