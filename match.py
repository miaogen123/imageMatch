# _*_ coding=utf-8 _*_
from math import sqrt
import cv2
import time
import os
import numpy as np
from scipy.stats.stats import  pearsonr
from collections import OrderedDict
from annoy import AnnoyIndex
#配置项文件
import  pymysql
from config import *
from mysql_config import *
from utils import getColorVec, Bdistance

db = pymysql.connect(DB_addr, DB_user, DB_passwod, DB_name )

def query(filename, rebuildAnnoy=False):
    if filename=="":
        fileToProcess=input("输入子文件夹中图片的文件名")
    else:
        fileToProcess=filename
    #fileToProcess="45.jpg"
    #TODO::修改文件输入的方式
    if(not os.path.exists(FOLDER+fileToProcess)):
        raise RuntimeError("文件不存在")
    start_time=time.time()
    img=cv2.imread(FOLDER+fileToProcess)
    colorVec1=getColorVec(img)
    #流式游标处理
    conn = pymysql.connect(host=DB_addr, user=DB_user, passwd=DB_passwod, db=DB_name, port=3306,
                           charset='utf8', cursorclass = pymysql.cursors.SSCursor)

    #TODO::使用pearsonr试试
    dataSet=AnnoyIndex(COLOR_DEGREE*COLOR_DEGREE*COLOR_DEGREE)
    dataSetFileName=TABLE_NAME+".ann"
    if os.path.exists(dataSetFileName) and not rebuildAnnoy:
        dataSet.load(dataSetFileName)
    else:
        with conn.cursor() as cursor:
            cursor.execute("select name, featureValue, id from "+TABLE_NAME+" order by name")
            row=cursor.fetchone()
            count=1
            while row is not None:
                colorVec2=row[1].split(',')
                colorVec2=list(map(eval, colorVec2))
                itemId=int(row[2])
                dataSet.add_item(itemId, colorVec2)
                count+=1
                row=cursor.fetchone()
                if count>200:
                    break
        dataSet.build(10)
        dataSet.save(dataSetFileName)
        end_time=time.time()
        time_cost=end_time-start_time
        print("buildind annoy set spends ", time_cost, ' s')
    resultSet=dataSet.get_nns_by_vector(colorVec1, 10)
    #从ID到文件名
    rela_name_dict=OrderedDict()
    getNameSet_sql="select name from "+TABLE_NAME+" where id in "+str(tuple(resultSet))
    with conn.cursor()  as cursor:
        cursor.execute(getNameSet_sql)
        rows=cursor.fetchall()
        for one in rows:
            print(one[0])
    #for one in resultSet: #dataSet.get_distance()


    #for one in range(0, MATCH_ITEM_NUM):
    #    print(namelist[one]+"\t\t"+str(float(Rlist[one])))


if __name__ == '__main__':
    #WriteDb()
    #exit()
    query("")

