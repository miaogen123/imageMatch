# _*_ coding=utf-8 _*_
from math import sqrt

__date__ = '9/24/2018 13:28 '

import cv2
import time
import os
import numpy as np
from  config import COLOR_DEGREE

def getColorVec(img):
    hei, width, channel=img.shape
    colorVec=[0 for e in range(0, int(pow(COLOR_DEGREE, 3)))]
    i=0
    while(i<hei):
        j=0
        while(j<width):
            pixel=img[i][j]
            grade=getPixelGrade(pixel)
            index=grade[0]*COLOR_DEGREE*COLOR_DEGREE+grade[1]*COLOR_DEGREE+grade[2]
            colorVec[index]+=1
            j+=1
        i+=1
    return colorVec


def getPixelGrade(pixel):
    grade=[]
    base=int(256/COLOR_DEGREE)+1
    for one in np.array(pixel):
        grade.append(int(one/base))
    return grade

def Bdistance(l1, l2):
    if(len(l1)!=len(l2)):
        raise RuntimeError("计算巴氏距离时，引入长度不相等的向量")
    s1=sum(l1)
    s2=sum(l2)
    BD=0
    for ind in range(0, len(l1)):
        BD+=sqrt((l1[ind]/s1)*(l2[ind]/s2))
    return BD


def pHash(imgfile):
    """get image pHash value"""
    #加载并调整图片为32x32灰度图片
    img=cv2.resize(imgfile,(64,64))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h,w), np.float32)
    vis0[:h,:w] = img[:h, :w]       #填充数据

    #二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    #cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    #vis1.resize(32,32)
    np.resize(vis1, (32, 32))

    #把二维list变成一维list
    img_list=np.ndarray.flatten(vis1)
    #img_list=[item for item in list for one in vis1]

    #计算均值
    avg = sum(img_list)*1./len(img_list)
    avg_list = ['0' if i<avg else '1' for i in img_list]

    #得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x+4]),2) for x in range(0,32*32,4)])


#文件后缀
def getFileSuffix(filename):
    return os.path.splitext(filename)[-1][1:]
#汉明距
def hammingDist(s1, s2):
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])
