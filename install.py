# -*- coding: UTF-8 -*-
# 用法
# python install.py

# 导入必要的包
import os									  # 文件和文件夹操作
import sys									  # 系统操作

# 显示欢迎信息
print("""

**********************************************************************************
 _   _  _      _                _____                _                            
| | | |(_)    | |              /  __ \              | |                           
| | | | _   __| |  ___   ___   | /  \/  __ _  _ __  | |_  _   _  _ __   ___  _ __ 
| | | || | / _` | / _ \ / _ \  | |     / _` || '_ \ | __|| | | || '__| / _ \| '__|
\ \_/ /| || (_| ||  __/| (_) | | \__/\| (_| || |_) || |_ | |_| || |   |  __/| |   
 \___/ |_| \__,_| \___| \___/   \____/ \__,_|| .__/  \__| \__,_||_|    \___||_|   
                                             | |                                  
*******************************************  |_|  ********************************
""")
print("")

# 设置循环
i = 0

while i == 0:
    # 询问用户是否开始安装
    answer = input("[i] 现在开始安装 video-capturer 依赖包？[y/n]").lower()

    if answer == "y":
        print("")

        # 首先安装或更新 pip
        os.system("python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple")

        # 要安装的依赖包
        libs = ["opencv-python", "imutils", "matplotlib", "colorama"]

        for lib in libs:
            os.system("pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple "+ lib)

        print("\n[v] 安装完成。")
        print("    如果有部分依赖包未安装成功，可以重新运行本程序。")
        print("    现在可以开始使用 video-capturer 了。")
        print("\a")
        i = 1

    elif answer == "n":
        print("[x] 您已取消安装 video-capturer 依赖包。")
        print("\a")
        i = 1

    else:
        print("\a")
        print("[x] 请输入 y 继续，或输入 n 取消。")
        i = 0