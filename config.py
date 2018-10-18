# _*_ coding=utf-8 _*_
__date__ = '9/24/2018 11:50 '

#默认会读取FOLDER下的所有文件
FOLDER="./image.vary.jpg/"
#支持的图片文件格式
ImageFormatSet=["jpeg", "jpg", "bmp", "png"]



#使用 基于直方图进行匹配时的参数调教
#每一个通道中细分的层数, 最终会形成COLOR_DEGREE^3中颜色
COLOR_DEGREE=11
TABLE_NAME_COM=COLOR_DEGREE*COLOR_DEGREE*COLOR_DEGREE
HISTOGRAM_TABLE_NAME="ImageMatchInfo_"+str(TABLE_NAME_COM)
#显示匹配的条目数量
MATCH_ITEM_NUM=10

#pHash算法
#table name
pHash_TABLE_NAME="pHash_feature"

#使用的table
TABLE_NAME=pHash_TABLE_NAME