## 自建图像检索引擎

-   可选的检索方法(不同的分支)
    -  颜色直方图(效果较差)
    -  采用annoy算法优化直方图向量的匹配过程(需要切换到BasedOnAnnoy分支), 因为annoy不支持动态添加，所以每次添加新的文件都要重新生成索引, 调用query时加上True参数即可(**很快**)
    -  **pHash:快, 但精度不高, 遍历9000张图的特征值进行256位汉明距计算，用时接近1s，还可以继续优化**,
      如果用c++重写的话，应该会快很多
-   特征提取&读入DB脚本
-   返回指定数量MATCH_ITEM_NUM （config.py) 条记录

<br>

## Usage:
1. 使用哪种方法就切换到那个分支

2. 在当前文件夹下创建一个mysql_config.py的文件, 其中应包含

   ```c++
     DB_name="XXXX"
     DB_addr="XXXX"
     DB_user="XXXX"
     DB_passwod="XXXX"
   ```


1. 导入base.sql 文件到mysql

2. 可以把所有的图片放在一个文件夹下面，然后修改config.py中的FOLDER变量，一次读入全部支持的图片格式

   ```python
     ImageFormatSet=["jpeg", "jpg", "bmp", "png"]
   ```

3. 使用readData.py 进行数据库的构建操作, **第一次运行会报错，按照提示修改base表的表名**

4. (服务器上)使用match.py 进行查询，输入当前文件夹下的文件名，本地读取，提取特征，由服务器进行检索，最终返回服务器数据库中最匹配的MATCH_ITEM_NUM条数据(config.py)

***
NOTE: 这个图像检索是多媒体的作业，我在颜色直方图基础上，为了提高效率和精度将他进行了扩充, 添加了pHash的检索和聚类优化，
形成了这样的一个简单的检索方案.\
实验报告pdf也上传在根目录下，里面有实现细	节

***

TODO: 

1. 针对phash 优化：选择将位分割，形成256位向量，利用annoy计算hanmming distance.
2. 选择Ann的分支在返回结果时，并没有对结果集按相关度进行排序，需要手动做
***
### 我的邮箱：miaogen156@gmail.com, 构建的时候有问题可以发邮件给我。welcome star！
