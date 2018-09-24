# _*_ coding=utf-8 _*_
__date__ = '9/24/2018 13:28 '


def getColorVec(img):
    hei, width, channel=img.shape
    colorVec=[0 for e in range(0, 64)]
    i=0
    while(i<hei):
        j=0
        while(j<width):
            pixel=img[i][j]
            grade=getPixelGrade(pixel)
            index=grade[0]*4*4+grade[1]*4+grade[2]
            colorVec[index]+=1
            j+=1
        i+=1
    return colorVec
