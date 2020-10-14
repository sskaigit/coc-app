import os
import time
import sys
import re
import json
import logging
from time import sleep
from os import system

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 获取的截图文件在手机中的保存位置(默认保存在内置存储根目录下)
# ANDRIOD_PIC_PATH = "/storage/emulated/0/tmp/screenshot.png"
ANDRIOD_PIC_PATH = "/storage/emulated/0/"  # /storage/emulated/0/dctp
# 文件保存在电脑中的目录
TRANS_PIC_PATH = "/Users/shaoshikai/Downloads/"
# 获取截图的adb命令
SCREEN_CAP_CMD = "adb shell screencap -p "
# 传输文件至电脑adb命令
TRANS_FILE_CMD = "adb pull "
# 获取Android手机分辨率命令
GET_RESOLUTION_CMD = "adb shell dumpsys window displays"
GET_RESOLUTION_CMD_PID = "adb -s %s shell dumpsys window displays"
# 模拟点击命令
POINT_SCREEN_CMD = "adb shell input tap"
# 手机分辨率
phoneResolution = []
GRID_PATH = "/Users/shaoshikai/develop/coc-app/resources/grid"

"""
获取设备屏幕分辨率
    adb devices 显示当前运行的全部模拟器
    deviceId 作为可变参数 表示是否传入设备的ID
"""
def getPhoneResolution(deviceId=None):
    if deviceId is None:
        # 如果没有传入指定设备ID，执行以下ADB command，获取设备屏幕分辨率
        r = os.popen(GET_RESOLUTION_CMD)
    else:
        # 如果传入指定设备ID，执行以下ADB command，获取设备屏幕分辨率
        r = os.popen(GET_RESOLUTION_CMD_PID % deviceId)
    # 获取命令行的打印值
    text = str(r.read())
    if not text:
        # 获取设备分辨率失败
        logging.error("Cannot get the resolution of screen, please check the ADB.")
        sys.exit()
    else:
        # 查找init=字符串，其后为手机分辨率情况
        beginC = text.find("init=")
        # 获取其后的10个字符
        line = text[beginC + 5:beginC + 15]
        resolution = line.split("x")
        logging.info(f"屏幕分辨率 X-{resolution[0]} Y-{resolution[1]}")
        phoneResolution.append(int(resolution[0]))
        phoneResolution.append(int(resolution[1]))
        size = [phoneResolution[0], phoneResolution[1]]
        r.close()
        return size

"""
模拟点击某一位置
    adb devices 显示当前运行的全部模拟器
    deviceId 作为可变参数 表示是否传入设备的ID
"""
def pointOnPhone(x=0.0, y=0.0):
    strX = str(x)
    strY = str(y)
    command = POINT_SCREEN_CMD + " " + strX + " " + strY
    system(command)
    # logging.info(f"模拟点击 X-{strX} Y-{strY}")

"""
模拟滑动
    adb devices 显示当前运行的全部模拟器
    deviceId 作为可变参数 表示是否传入设备的ID
    t=100 作为可变参数 表示默认的滑动时间为100ms 可自寻设计滑动时间
    n=1 作为可变参数 表示默认的滑动次数为1次 可自寻设计滑动次数
"""
def slideOnPhone(x1=0.0, y1=0.0, x2=0.0, y2=0.0, t=100, n=1, deviceId=None):
    for i in range(n):
        if deviceId is None:
            os.system("adb shell input swipe %f %f %f %f %d" % (x1, y1, x2, y2, t))
        else:
            os.system("adb -s %s shell input swipe %f %f %f %f %d" % (deviceId, x1, y1, x2, y2, t))
    # logging.info(f"模拟滑动点击 X1-{x1} Y1-{y1} X2-{x2} Y2-{y2} 滑动时间-{t} 点击次数-{n} deviceId-{deviceId}")

"""
保存截图至手机
    fileName 必填参数 表示保存文件名
    andriodPicPath 可选参数 表示保存手机目录地址
"""
def getPhoneScreen(fileName, andriodPicPath=None):
    path = andriodPicPath if andriodPicPath is not None else ANDRIOD_PIC_PATH
    # 获取屏幕截图
    command = SCREEN_CAP_CMD + path + fileName
    system(command)
    logging.info(f"保存屏幕截图 path-{path} fileName-{fileName}")

"""
传送文件至电脑
    andriodFileName 必填参数 表示手机上传文件名
    transFileName 必填参数 表示电脑保存文件名
    andriodPicPath 作为可变参数 表示上传图片的手机地址
    transPicPath 作为可变参数 表示电脑保存地址
"""
def transPhoneScreen(andriodFileName, transFileName, andriodPicPath=None, transPicPath=None):
    # 将截图传输至电脑
    andriodPath = andriodPicPath if andriodPicPath is not None else ANDRIOD_PIC_PATH
    transPath = transPicPath if transPicPath is not None else TRANS_PIC_PATH
    command = TRANS_FILE_CMD + andriodPath + andriodFileName + " " + transPath + transFileName
    system(command)
    logging.info(f"传送文件至电脑 path-{transPath} andriodFileName-{andriodFileName} transFileName-{transFileName}")

"""
训练部队
    data 必填 部队缺少兵种 例：['1-barbarian', '2-archer']
"""
def train_troops(data, type):
    path = GRID_PATH + '/troops_grid.json'
    if type == 'magic':
        path = GRID_PATH + '/magic_grid.json'
    elif type == 'machine':
        path = GRID_PATH + '/machine_grid.json'

    troops_grid = json.load(open(path))
    grids = []
    if len(data) > 0:
        for i in data:
            grids.append(troops_grid[i])
    if len(grids) > 0:
        for grid in grids:
            slideOnPhone(grid[0], grid[1], grid[0], grid[1])

if __name__ == '__main__':
    # 一、获取分辨率
    size = getPhoneResolution()
    print(size)

    # 二、模拟点击
    # pointOnPhone(1002, 887)

    # slideOnPhone(700,600,700,1800)
    # time.sleep(3)
    # pointOnPhone(30,503)

    # 三、模拟滑动
    # x1 = size[0] * 0.187   #202/1080  注：这里的x,y和调试手机指针的x,y是反的
    # y1 = size[1] * 0.351   #673/1920
    # x2 = size[0] * 0.187
    # y2 = size[1] * 0.351
    # slideOnPhone(x1, y1, x2, y2, 50, 3)

    # 四、保存截图至手机
    # getPhoneScreen("screenshot.png")

    # 五、传送文件至电脑
    # transPhoneScreen(andriodFileName="screenshot.png",transFileName="screenshot.png")

    # 六、训练部队
    # train_troops(['8-skeleton', '9-bat'], "magic")
