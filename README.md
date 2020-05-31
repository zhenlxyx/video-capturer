# video-capturer
 从视频中捕捉包含运动的画面

## 系统支持

* Windows, macOS, Linux
* Python 3 以上
* OpenCV 3 或以上

## 开始使用之前

以 Windows 10 为例：

1. 安装 Python

   打开 Microsoft Store 应用，搜索“Python”并下载 Python 3.7 / 3.8。

2. 安装 OpenCV

   打开命令提示符或 PowerShell，输入 pip install opencv-python 并回车，等待安装完成。

3. 安装 imutils

   打开命令提示符或 PowerShell，输入 pip install imutils 并回车，等待安装完成。

4. 安装 matplotlib

   打开命令提示符或 PowerShell，输入 pip install matplotlib 并回车，等待安装完成。
   
5. 安装 colorama

   打开命令提示符或 PowerShell，输入 pip install colorama 并回车，等待安装完成。

为防止因权限不足，无法进行文件或文件夹而中断采集，建议以管理员身份运行命令提示符或 PowerShell。

pythonw

类似的视频（例如从同一个摄像头）可以批处理。如果另一些视频差异太大，可能需要修改 JSON 配置以调整采集精度。