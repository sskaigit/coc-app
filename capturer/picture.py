import aircv
import cv2 as cv
from PIL import Image
import numpy as np

"""
识别小图在大图中的匹配值（灰度处理）
    :param bigFilePath: 大图路径 例：/Users/shaoshikai/Downloads/help_Troops.png
    :param smallFilePath: 小图路径 例：/Users/shaoshikai/develop/coc-app/resources/troopsPicture/12-digger.png
    :return 匹配值  大于0.9即可认为小图在大图中出现（匹配值可根据实际情况调整）
"""
def match_picture(bigFilePath, smallFilePath):
    img = cv.imread(bigFilePath)
    template = cv.imread(smallFilePath)
    # 图片灰度处理。
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    # 匹配
    result = cv.matchTemplate(img_gray, template_gray, cv.TM_CCOEFF_NORMED)
    # maxres大于0.9即可认为模板在匹配图像中出现
    return result.max() 

"""
识别小图在大图中位置，并画出区域显示
    :param bigFilePath: 大图路径 例：/Users/shaoshikai/Downloads/help_Troops.png
    :param smallFilePath: 小图路径 例：/Users/shaoshikai/develop/coc-app/resources/troopsPicture/12-digger.png
"""
def match_picture_show(bigFilePath, smallFilePath):
    img = cv.imread(bigFilePath)
    template = cv.imread(smallFilePath)
    # 图片灰度处理。
    # img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 匹配
    result = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    
    # max_loc为左上角
    # 右下角
    h, w = template.shape[:2]
    right_bottom = (max_loc[0] + w, max_loc[1] + h)

    print(max_loc)
    print(right_bottom)
    # 画矩形,红色的线框出来。
    cv.rectangle(img=img, pt1=max_loc, pt2=right_bottom, color=(0, 0, 255), thickness=3)
 
    cv.imshow('result', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

"""
（不太稳定）图片对比识别imgobj在imgsrc上的相对位置（批量识别统一图片中需要的部分）
    :param imgsrc: 原始图片路径(str)
    :param imgobj: 待查找图片路径（模板）(str)
    :param confidence: 识别度（0<confidence<1.0）
    :return: None or dict({'confidence': 相似度(float), 'rectangle': 原始图片上的矩形坐标(tuple), 'result': 中心坐标(tuple)})
"""
def matchImg(imgsrc, imgobj, confidence=0.4):
    imsrc = aircv.imread(imgsrc)
    imobj = aircv.imread(imgobj)

    match_result = aircv.find_template(imsrc, imobj, confidence)  
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

    return match_result

"""
识别图片是否为灰度
"""
def is_gray(img, threshold=10):
    if len(img.getbands()) == 1:
        return True
    img1 = np.asarray(img.getchannel(channel=0), dtype=np.int16)
    img2 = np.asarray(img.getchannel(channel=1), dtype=np.int16)
    img3 = np.asarray(img.getchannel(channel=2), dtype=np.int16)
    diff1 = (img1 - img2).var()
    diff2 = (img2 - img3).var()
    diff3 = (img3 - img1).var()
    diff_sum = (diff1 + diff2 + diff3) / 3.0
    if diff_sum <= threshold:
        return True
    else:
        return False

"""
灰度处理图片
    :param imgSrc: 待处理的图片路径 例：/Users/shaoshikai/develop/coc-app/data/troops-1.png
    :param imgSave: 灰度处理后的图片路径 例：/Users/shaoshikai/develop/coc-app/data/troops-12.png
"""
def gray_img(imgSrc, imgSave):
    im = Image.open(imgSrc)
    im_gray = im.convert('L')
    im_gray.save(imgSave)

if __name__ == "__main__":
    # maxres = match_picture("/Users/shaoshikai/develop/coc-app/data/chat.png", "/Users/shaoshikai/develop/coc-app/data/help.png")
    # maxres = match_picture("/Users/shaoshikai/develop/coc-app/data/troops-1.png", "/Users/shaoshikai/develop/coc-app/resources/troopsPicture/3-giant.png")
    # print(maxres)
 
    # img = Image.open('/Users/shaoshikai/Downloads/22.png')
    # r = is_gray(img)
    # print(r)

    # match_result = matchImg("/Users/shaoshikai/Downloads/b.png","/Users/shaoshikai/Downloads/help_Troops.png")
    # print(match_result)

    gray_img('/Users/shaoshikai/develop/coc-app/data/troops-1.png','/Users/shaoshikai/develop/coc-app/data/troops-12.png')