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
from mysql_config import *
from utils import getColorVec, Bdistance,hammingDist, pHash

db = pymysql.connect(DB_addr, DB_user, DB_passwod, DB_name )

def query(filename):
    if filename=="":
        fileToProcess=input("输入子文件夹中图片的文件名")
    else:
        fileToProcess=filename
    #fileToProcess="45.jpg"
    if(not os.path.exists(FOLDER+fileToProcess)):
        raise RuntimeError("文件不存在")
    start_time=time.time()
    img=cv2.imread(FOLDER+fileToProcess)
    phash1=pHash(img)

    #测试：主观相似的图像的pHash的汉明距
    #for e in range(7284, 7301):
    #    file=str(e)+".jpg"
    #    img2=cv2.imread(FOLDER+file)
    #    phash2=pHash(img2)
    #    print(file, ":", hammingDist(phash1,phash2))

    #exit(1)
    #流式游标处理
    conn = pymysql.connect(host=DB_addr, user=DB_user, passwd=DB_passwod, db=DB_name, port=3306,
                           charset='utf8', cursorclass = pymysql.cursors.SSCursor)
    leastNearRInFive=256+1

    Rlist=[]
    namelist=[]
    init_str="k"
    for one in range(0, MATCH_ITEM_NUM):
        #因为phash的汉明距越小越匹配, 初始集中设置大值
        Rlist.append(256+1)
        namelist.append(init_str)

    with conn.cursor() as cursor:
        cursor.execute("select name, featureValue from "+pHash_TABLE_NAME+" order by name")
        row=cursor.fetchone()
        count=1
        while row is not None:
            if row[0] == fileToProcess:
                row=cursor.fetchone()
                continue
            phash2=row[1]
            rela=hammingDist(phash1, phash2)

            if rela<leastNearRInFive:
                index=0
                for one in Rlist:
                    if rela <one:
                        Rlist.insert(index, rela)
                        Rlist.pop(MATCH_ITEM_NUM)
                        namelist.insert(index, row[0])
                        namelist.pop(MATCH_ITEM_NUM)
                        leastNearRInFive=Rlist[MATCH_ITEM_NUM-1]
                        break
                    index+=1
            count+=1
            row=cursor.fetchone()
    end_time=time.time()
    time_cost=end_time-start_time
    print("spend ", time_cost, ' s')
    for one in range(0, MATCH_ITEM_NUM):
        print(namelist[one]+"\t\t"+str(float(Rlist[one])))


if __name__ == '__main__':
    #WriteDb()
    #exit()
    query("")

