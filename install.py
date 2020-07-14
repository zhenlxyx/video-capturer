# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# 用法

'''
开始安装
python install.py

如果上述命令出现错误，请输入以下命令开始安装
python3 install.py
'''

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
（安装程序）


[i] 本程序将安装下列 video-capturer 依赖包到你的电脑上：
     - opencv-python
     - imutils
     - imagezmq
     - matplotlib
     - colorama
     - keyboard（如果在 Windows 运行）

    部分依赖包可能需要管理员权限，已安装的依赖包将被更新或覆盖。
""")

# 设置循环
i = 0

while i == 0:
    # 询问用户是否开始安装
    answer = input("    现在开始安装 video-capturer 依赖包？[y/n]").lower()

    if answer == "y":
        print("\n\n[i] 安装已开始。\n")

        try:
            # 首先安装或更新 pip
            print("\n[i] 正在设置 pip 包安装工具...\n")
            os.system("python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple")

            # 要安装的依赖包
            libs = ["opencv-python", "imutils", "imagezmq", "matplotlib", "colorama"]
            counter = 0

            for lib in libs:
                counter += 1
                print("\n[i] 正在安装 ({}/{})：{}...\n".format(counter, len(libs), libs[counter - 1]))
                os.system("python3 -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple "+ lib)

            if os.name == 'nt':
                print("\n[i] 正在安装额外项：keyboard...\n")
                os.system("python3 -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple keyboard")

        except:
            # 首先安装或更新 pip
            print("\n[i] 正在设置 pip 包安装工具...\n")
            os.system("python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple")

            # 要安装的依赖包
            libs = ["opencv-python", "imutils", "imagezmq", "matplotlib", "colorama"]
            counter = 0

            for lib in libs:
                counter += 1
                print("\n[i] 正在安装 ({}/{})：{}...\n".format(counter, len(libs), libs[counter - 1]))
                os.system("python -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple "+ lib)

            if os.name == 'nt':
                print("\n[i] 正在安装额外项：keyboard...\n")
                os.system("python -m pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple keyboard")   

        print("\n\n[v] 安装完成。现在可以开始使用 video-capturer 了。")
        print("    如果有部分依赖包未安装成功，可以重新运行本程序，或使用")
        print("        pip install 安装包名称")
        print("    命令来安装它。")
        print("\a")
        i = 1

    elif answer == "n":
        print("\n\n[x] 您已取消安装 video-capturer 依赖包。")
        print("\a")
        i = 1

    else:
        print("    请输入 y 继续，或输入 n 取消。")
        print("\a")
        i = 0