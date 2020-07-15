# 导入必要的包
import imutils
import cv2

class BiFrameMotionDetector:
	def __init__(self, accumWeight=0.5, deltaThresh=5, minArea=5000):
		# 确定 OpenCV 版本、帧累积权重、阈值增量最小值、轮廓区域最小值
		self.isv2 = imutils.is_cv2()
		self.accumWeight = accumWeight
		self.deltaThresh = deltaThresh
		self.minArea = minArea

		# 初始化运动检测的前一帧
		self.lastFrame1 = None

	def update(self, image):
		# 初始化包含运动的位置列表
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

		# 使用适当版本的 OpenCV 在阈值图像中查找轮廓
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# 遍历轮廓
		for c in cnts:
			# 仅在轮廓大于轮廓区域最小值时，将其添加到位置列表中
			if cv2.contourArea(c) > self.minArea:
				locs.append(c)
		
		# 返回位置列表
		return locs