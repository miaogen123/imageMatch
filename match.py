from math import sqrt
import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
#配置项文件
from .config import *
from .utils import getColorVec
import  pymysql

FOLDER="./image.vary.jpg/"
db = pymysql.connect(DB_addr,DB_user,DB_passwod,DB_name )


if __name__ == '__main__':
    #WriteDb()
    #exit()
    start_time=time.time()
    fileToProcess=input("输入子文件中图片的文件名")
    #fileToProcess="45.jpg"
    if(not os.path.exists(FOLDER+fileToProcess)):
        raise RuntimeError("文件不存在")
    img=cv2.imread(FOLDER+fileToProcess)
    colorVec1=getColorVec(img)
    #流式游标处理
    conn = pymysql.connect(host=DB_addr, user=DB_user, passwd=DB_passwod, db=DB_name, port=3306,
                       charset='utf8', cursorclass = pymysql.cursors.SSCursor)
    leastNearRInFive=0

    Rlist=[]
    namelist=[]
    init_str="k"
    for one in range(0, 5):
        Rlist.append(0)
        namelist.append(init_str)
        init_str+="k"

    with conn.cursor() as cursor:
        cursor.execute("select name, featureValue from ImageMatchInfo order by name")
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
                        Rlist.pop(5)
                        namelist.insert(index, row[0])
                        namelist.pop(5)
                        leastNearRInFive=Rlist[4]
                        break
                    index+=1
            count+=1
            row=cursor.fetchone()
    end_time=time.time()
    time_cost=end_time-start_time
    print("spend ", time_cost, ' s')
    for one in range(0, 5):
        print(namelist[one]+"\t"+str(float(Rlist[one])))


