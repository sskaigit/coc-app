import os
import time
import tkinter
import cv2
from PIL import Image, ImageSequence, ImageDraw, ImageFont

import pyautogui
pyautogui.PAUSE = 0.5 

# 指定要使用的字体和大小；/Library/Fonts/是macOS字体目录；Linux的字体目录是/usr/share/fonts/
font = ImageFont.truetype('./resources/simsun001.TTF', 35)

def picture_cut(filePath, fileName, text=None, region=None):
    file = f'{filePath}/{fileName}'
    if not os.path.exists(filePath):
        os.makedirs(filePath)

    # 截图
    cut(file, region)

    # 图片加文字
    if text is not None:
        im_before = Image.open(file)
        im_after = add_text_to_image(im_before, text)
        im_after.save(file)

def cut(file, region):
    screen = tkinter.Tk()
    #获取当前屏幕的宽
    x_width = screen.winfo_screenwidth()
    #获取当前屏幕的高
    y_height = screen.winfo_screenheight()
    y = y_height // 10
    print(x_width, y)
    if region is None:
        pyautogui.screenshot(file, region=[0, y, x_width, y_height-y])
    else:
        pyautogui.screenshot(file, region)

# image: 图片  text：要添加的文本 font：字体
def add_text_to_image(image, text, font=font):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    x = (rgba_image.size[0] - text_size_x)
    y = (rgba_image.size[1] - text_size_y) * 0.1
    # 设置文本颜色和透明度
    image_draw.text((x,y), text, font=font, fill=(255,33,33), stroke_width=1)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text

"""
图片裁剪
    cropFile 作为必填参数 需要裁剪的图片 例：/Users/shaoshikai/Downloads/screenshot.png
    saveFile 作为必填参数 裁剪后保存地址 例：/Users/shaoshikai/Downloads/screenshot.png
    grid 作为必填参数 裁剪坐标，从左顺时针到下(left, upper, right, lower) 例：(0, 0, 512, 128)
"""
def picture_crop(cropFile, saveFile, grid):
    img = Image.open(cropFile)
    cropped = img.crop(grid) 
    cropped.save(saveFile)

if __name__ == '__main__':
    # os.system("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome https://login.taobao.com/member/login.jhtml")
    # time.sleep(2)
    # picture_cut("/Users/shaoshikai/java/rpa-app/picture/", "test.png", "20200923120139")

    picture_crop("/Users/shaoshikai/Downloads/screenshot.png","/Users/shaoshikai/Downloads/screenshot.png", (0, 0, 512, 128))
