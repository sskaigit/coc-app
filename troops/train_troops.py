import os
import sys
import json
import time
import logging
import schedule
from PIL import Image
sys.path.append('/Users/shaoshikai/develop/coc-app')
from util.adb_util import *
from capturer.capture import *
from capturer.picture import *

import pyperclip
import pyautogui
pyautogui.PAUSE = 0.5 

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_FILE_PATH = "/Users/shaoshikai/develop/coc-app/data/"
RESOURCES_PATH = "/Users/shaoshikai/develop/coc-app/resources"
# 军队概况,缺少部队的图片匹配值
MATCH_VALUE = 0.9

def support_troops():
    base_grid = json.load(open(f"{RESOURCES_PATH}/grid/base_grid.json"))
    # 一、打开聊天窗口
    chat_open = base_grid['chat_open']
    slideOnPhone(chat_open[0], chat_open[1], chat_open[0], chat_open[1])

    # 二、识别增援按钮坐标，并点击增援  （TODO 后期可滑动聊天窗口，防止遗漏）
    flag = confirm_help_grid()
    if flag == False:
        return

    # 三、关闭聊天窗口
    chat_close = base_grid['chat_close']
    slideOnPhone(chat_close[0], chat_close[1], chat_close[0], chat_close[1])

    # 四、打开训练窗口
    train_icon = base_grid['train_icon']
    slideOnPhone(train_icon[0], train_icon[1], train_icon[0], train_icon[1])

    # 五、截图，军队概况
    time.sleep(3)
    capturer_troops()

    # 六、确认缺少部队
    time.sleep(3)
    lack_troops = confirm_lack_troops()
    lack_magic = confirm_lack_magic()
    lack_machine = confirm_lack_machine()

    # 七、训练缺少部队
    train_troop = base_grid['train_troops']
    slideOnPhone(train_troop[0], train_troop[1], train_troop[0], train_troop[1])
    train_troops(lack_troops, 'troops')

    train_magic = base_grid['train_magic']
    slideOnPhone(train_magic[0], train_magic[1], train_magic[0], train_magic[1])
    train_troops(lack_magic, 'magic')

    train_machine = base_grid['train_machine']
    slideOnPhone(train_machine[0], train_machine[1], train_machine[0], train_machine[1])
    train_troops(lack_machine, 'machine')

    # 八、关闭训练窗口 
    slideOnPhone(train_icon[0], train_icon[1], train_icon[0], train_icon[1])

"""
一、训练部队，部队列表往右滑
"""
def train_swipe(direction):
    if direction == 'right':
        slideOnPhone(930,870,1880,870)
    else:
        slideOnPhone(1880,870,930,870)

"""
二、军队概况（法术），列表往右滑
"""
def magic_swipe(direction):
    if direction == 'right':
        slideOnPhone(800,600,1200,600)
    else:
        slideOnPhone(1200,600,800,600)

"""
三、军队概况（部队），列表往右滑
"""
def troops_swipe(direction):
    if direction == 'right':
        slideOnPhone(800,300,1150,300)
    else:
        slideOnPhone(1150,300,800,300)

"""
四、截图，军队概况
"""
def capturer_troops():
    for i in range(0, 3):
        if i == 0:
            getPhoneScreen("screenshot.png")  
            transPhoneScreen(andriodFileName="screenshot.png",transFileName=f"screenshot.png", transPicPath=BASE_FILE_PATH)
            # 切割
            picture_crop(f'{BASE_FILE_PATH}screenshot.png',f'{BASE_FILE_PATH}troops-1.png',(242,195,1430,383))
            picture_crop(f'{BASE_FILE_PATH}screenshot.png',f'{BASE_FILE_PATH}magic-1.png',(242,486,1314,677))
            picture_crop(f'{BASE_FILE_PATH}screenshot.png',f'{BASE_FILE_PATH}machine.png',(1507,191,1947,383))
        elif i == 1:
            troops_swipe("left")
            magic_swipe("left")
            getPhoneScreen("screenshot.png")
            transPhoneScreen(andriodFileName="screenshot.png",transFileName=f"screenshot.png", transPicPath=BASE_FILE_PATH)
             # 切割
            picture_crop(f'{BASE_FILE_PATH}screenshot.png',f'{BASE_FILE_PATH}troops-2.png',(242,195,1430,383))
            picture_crop(f'{BASE_FILE_PATH}screenshot.png',f'{BASE_FILE_PATH}magic-2.png',(242,486,1314,677))
        else:
            troops_swipe("left")
            getPhoneScreen("screenshot.png")
            transPhoneScreen(andriodFileName="screenshot.png",transFileName=f"troops-3.png", transPicPath=BASE_FILE_PATH)
            picture_crop(f'{BASE_FILE_PATH}troops-3.png',f'{BASE_FILE_PATH}troops-3.png',(242,195,1430,383))

"""
五、确认缺少部队
"""
def confirm_lack_troops():
    data=[]
    picPath = RESOURCES_PATH + '/troopsPicture'
    img_list = os.listdir(picPath)
    # 按创建时间排序
    img_list.sort(key=lambda fn: os.path.getctime(picPath+'/'+fn))
    for inx, f in enumerate(img_list):
        file_path = os.path.join(picPath, f)
        if inx < 7: 
            maxres = match_picture(BASE_FILE_PATH+"troops-1.png", file_path)
            if maxres < MATCH_VALUE:
                data.append(f.replace('.png',''))
        elif 7 <= inx <= 10:
            # coords1 = pyautogui.locateAll(file_path, BASE_FILE_PATH+"troops-1.png", grayscale=False)
            # coords2 = pyautogui.locateAll(file_path, BASE_FILE_PATH+"troops-2.png", grayscale=False)
            # if int(len(list(coords1))) +  int(len(list(coords2))) < 1:
            maxres1 = match_picture(BASE_FILE_PATH+"troops-1.png", file_path)
            maxres2 = match_picture(BASE_FILE_PATH+"troops-2.png", file_path)
            if maxres1 < MATCH_VALUE and maxres2 < MATCH_VALUE:
                data.append(f.replace('.png',''))
        elif inx <= 14:
            maxres = match_picture(BASE_FILE_PATH+"troops-2.png", file_path)
            if maxres < MATCH_VALUE:
                data.append(f.replace('.png',''))
        elif 15 <= inx <= 19:
            maxres1 = match_picture(BASE_FILE_PATH+"troops-2.png", file_path)
            maxres2 = match_picture(BASE_FILE_PATH+"troops-3.png", file_path)
            if maxres1 < MATCH_VALUE and maxres2 < MATCH_VALUE:
                data.append(f.replace('.png',''))
        else:
            # coords = pyautogui.locateAll(file_path, BASE_FILE_PATH+"troops-3.png", grayscale=False)
            # if len(list(coords)) == 0:
            maxres = match_picture(BASE_FILE_PATH+"troops-3.png", file_path)
            if maxres < MATCH_VALUE:
                data.append(f.replace('.png',''))
    logging.info(f"（军队概况）窗口，（部队）缺少详情 data-{data}")
    return data

"""
六、确认缺少法术
"""
def confirm_lack_magic():
    data=[]
    picPath = RESOURCES_PATH + '/magicPicture'
    img_list = os.listdir(picPath)
    # 按创建时间排序
    img_list.sort(key=lambda fn: os.path.getctime(picPath+'/'+fn))
    for inx, f in enumerate(img_list):
        file_path = os.path.join(picPath, f)
        if inx <= 6: 
            maxres = match_picture(BASE_FILE_PATH+"magic-1.png", file_path)
            if maxres < MATCH_VALUE:
                data.append(f.replace('.png',''))
        else:
            # coords = pyautogui.locateAll(file_path, BASE_FILE_PATH+"magic-2.png", grayscale=False)
            # if len(list(coords)) == 0:
            maxres = match_picture(BASE_FILE_PATH+"magic-2.png", file_path)
            if maxres < MATCH_VALUE:
                data.append(f.replace('.png',''))
    logging.info(f"（军队概况）窗口，（法术）缺少详情 data-{data}")
    return data

"""
七、确认缺少攻城机器
"""
def confirm_lack_machine():
    data=[]
    picPath = RESOURCES_PATH + '/machinePicture'
    img_list = os.listdir(picPath)
    for f in img_list:
        file_path = os.path.join(picPath, f)
        maxres = match_picture(BASE_FILE_PATH+"machine.png", file_path)
        if maxres < MATCH_VALUE:
            data.append(f.replace('.png',''))
    logging.info(f"（军队概况）窗口，（攻城机器）缺少详情 data-{data}")
    return data

"""
八、确认增援请求
"""
def confirm_help_grid():
    getPhoneScreen("screenshot.png")
    transPhoneScreen(andriodFileName="screenshot.png",transFileName="chat.png", transPicPath=BASE_FILE_PATH)

    coords = pyautogui.locateAll(RESOURCES_PATH+"/help/help2.png", BASE_FILE_PATH+"chat.png", grayscale=False)
    logging.info(f"（聊天）窗口，增援请求个数 count-{len(list(coords))}")
    flag = False
    for i in list(coords):
        x_location, y_location = pyautogui.center(i)
        slideOnPhone(x_location, y_location, x_location, y_location)
        # 默认点击三行三列
        pointOnPhone(876, 196)
        pointOnPhone(876, 375)
        pointOnPhone(876, 595)
        pointOnPhone(1015, 196)
        pointOnPhone(1015, 375)
        pointOnPhone(1015, 595)
        pointOnPhone(1150, 196)
        pointOnPhone(1150, 375)
        pointOnPhone(1150, 595)
        slideOnPhone(x_location, y_location, x_location, y_location)
        flag = True
    return flag

def train_job():
    support_troops()

schedule.every(10).minutes.do(train_job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()

    # 一、左右滑动
    # train_swipe("right")
    # magic_swipe("left")
    # troops_swipe("left")
    # 二、训练营截图
    # capturer_troops()
    # 三、识别部队缺失兵种
    # data=confirm_lack_troops()
    # data=confirm_lack_magic()
    # data=confirm_lack_machine()
    # print(data)
    # 四、图片切割，并比较小图是否存在
    # picture_crop("/Users/shaoshikai/develop/coc-app/resources/troopsPicture/3-giant.png","/Users/shaoshikai/develop/coc-app/resources/troopsPicture/3-giant2.png",(0,33,128,150))
    # coords = pyautogui.locate("/Users/shaoshikai/develop/coc-app/resources/troopsPicture/2-archer.png", "/Users/shaoshikai/develop/coc-app/data/troops-1.png", grayscale=True)
    # print(coords)
    # 五、确认请求坐标，并增援
    # flag = confirm_help_grid()
    