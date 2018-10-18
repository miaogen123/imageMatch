# _*_ coding=utf-8 _*_
__date__ = '9/24/2018 13:22 '

import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
#配置项文件
from config import *
from utils import getColorVec, getFileSuffix, pHash
from mysql_config import  *

import  pymysql

db = pymysql.connect(DB_addr,DB_user,DB_passwod,DB_name )
MAX_TO_COMMIT=500

#读取folderPath下的所有文件
def readFileInCurrentFolder(folderPath):
    all=os.listdir(folderPath)
    files=[]
    for file in  all:
        if not os.path.isdir(file) and getFileSuffix(file) in ImageFormatSet :
            files.append(file)
    return files


def WriteDb(filename):
    if filename!="":
        if getFileSuffix(filename) not in ImageFormatSet:
            return
        fileSet=[filename]
    else:
        fileSet=readFileInCurrentFolder(FOLDER)
    ISFORMAT="%Y-%m-%d %H:%M:%S"
    maxToCommit=0
    cursor=db.cursor()
    start_time=time.time()
    for file in fileSet:
        img=cv2.imread(FOLDER+file)
        if img.ndim !=3:
            raise RuntimeError("图像维数不为3")
        filestat=os.stat(FOLDER+file)
        modified_time_ori=time.localtime(filestat.st_mtime)
        modified_time= time.strftime(ISFORMAT, modified_time_ori)
        size=filestat.st_size
        sqlstat="insert into "+TABLE_NAME+" (name, size, modified_time, featureValue) value (%s, %s, %s, %s)"

        toGetTuple=[file, size, modified_time, pHash(img)]
        try:
            cursor.execute(sqlstat, tuple(toGetTuple))
        except Exception as e:
            print(e)
        finally:
            #TODO::删掉下面一行
            db.commit()
            maxToCommit+=1
            if maxToCommit>MAX_TO_COMMIT:
                db.commit()
                end_time=time.time()
                print(end_time-start_time, " s")
                start_time=end_time
                maxToCommit=0


if __name__ == '__main__':
    #filename=input("请输入想要读的文件的路径, 不输入即读取"+FOLDER+"下的所有文件")
    filename=""
    WriteDb(filename)

