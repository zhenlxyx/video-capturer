# 导入必要的包
import imutils
import cv2

class TriFrameMotionDetector:
	def __init__(self, accumWeight=0.5, deltaThresh=5, minArea=5000):
		# 确定 OpenCV 版本、帧累积权重、阈值增量最小值、轮廓区域最小值
		self.isv2 = imutils.is_cv2()
		self.accumWeight = accumWeight
		self.deltaThresh = deltaThresh
		self.minArea = minArea

		# 初始化运动检测的前两帧
		self.lastFrame1 = None
		self.lastFrame2 = None

	def update(self, image):
		# 初始化包含运动的位置列表
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