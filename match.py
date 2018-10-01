# _*_ coding=utf-8 _*_
from math import sqrt
import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
#配置项文件
import  pymysql
from config import *
from utils import getColorVec

db = pymysql.connect(DB_addr, DB_user, DB_passwod, DB_name )

def query(filename):
    if filename=="":
        fileToProcess=raw_input("输入子文件夹中图片的文件名")
    else:
        fileToProcess=filename
    #fileToProcess="45.jpg"
    if(not os.path.exists(FOLDER+fileToProcess)):
        raise RuntimeError("文件不存在")
    start_time=time.time()
    img=cv2.imread(FOLDER+fileToProcess)
    colorVec1=getColorVec(img)
    #流式游标处理
    conn = pymysql.connect(host=DB_addr, user=DB_user, passwd=DB_passwod, db=DB_name, port=3306,
                           charset='utf8', cursorclass = pymysql.cursors.SSCursor)
    leastNearRInFive=0

    Rlist=[]
    namelist=[]
    init_str="k"
    for one in range(0, MATCH_ITEM_NUM):
        Rlist.append(0)
        namelist.append(init_str)
        init_str+="k"

    with conn.cursor() as cursor:
        cursor.execute("select name, featureValue from ImageMatchInfo_1331 order by name")
        row=cursor.fetchone()
        count=1
        while row is not None:
            if row[0] == fileToProcess:
                row=cursor.fetchone()
                continue
            colorVec2=row[1].split(',')
            colorVec2=list(map(eval, colorVec2))
            R2=pearsonr(colorVec1, colorVec2)
            if abs(R2[0])>abs(leastNearRInFive):
                index=0
                for one in Rlist:
                    if R2[0] >one:
                        Rlist.insert(index, R2[0])
                        Rlist.pop(MATCH_ITEM_NUM)
                        namelist.insert(index, row[0])
                        namelist.pop(MATCH_ITEM_NUM)
                        leastNearRInFive=Rlist[4]
                        break
                    index+=1
            count+=1
            row=cursor.fetchone()
    end_time=time.time()
    time_cost=end_time-start_time
    print("spend ", time_cost, ' s')
    for one in range(0, MATCH_ITEM_NUM):
        print(namelist[one]+"\t"+str(float(Rlist[one])))


if __name__ == '__main__':
    #WriteDb()
    #exit()
    query("")

