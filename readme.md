针对遥感图像的车道线检测
==========
算法的流程主要包括对车牌的预处理（高斯滤波）、直线提取（边缘检测、霍夫变换）、直线过滤。最后输出检测得到的车道结果。

预处理
---------
就是高斯滤波，因为不滤波的话canny的结果干扰比较多，会影响直线检测。滤波窗口大小这个参数是有一定作用的，太小了滤不掉，太大了的话就把车道线滤掉了

直线提取
-----------
边缘检测用的是canny算子。canny这参数是最重要的，如果设置不当会出现很多杂线或者没检测出车道线。霍夫变换就是正常变没啥说的

直线过滤
----------
霍夫变换的结果还需要处理，因为车道线检测不等于直线检测。图里还有其它的部分可能会构成直线。所以这里需要滤一下。因为是遥感照片，所以检测出的大部分直线都是顺着车道线方向的，所以可以利用斜率均值过滤。就是基于均值，斜率在一个标准差范围内的才算是我们检测出的这个直线

寻找最优参数组合
--------
因为不同图片它特点不太一样，所以对于不同图片可能得用不同的参数才能弄出最好的检测效果。所以自动调参是有必要的。调参这个有两种策略，一个是正向策略，通过图像特征决定我要用什么参数。但这个特征是很难找的。另外就是反向，根据检测结果看现在这参数好不好，然后再调。如果要用反向方法，就得有一个针对检测结果的评价指标。这里我选择的是滤掉直线的比例，滤掉的比例越高说明这次检测的结果越不好。那要是效果不好，我就迭代调整canny的参数。具体做法是当滤掉直线比例大于阈值时，重新调用检测车道线函数，并记录调用次数。canny参数按调用次数以一个固定速率变化，对边缘检测进行更严格的限制

今后工作
-----------
目前没法检测车道上的虚线以及各种标志。因为虚线和标志一般不太明显，需要识别范围更大的参数组合，但这样容易产生杂线。因此需要线基于canny结果生成mask，框出道路，然后再使用识别范围更大的参数组合对道路内部进行检测。并手动连接虚线。这个目前还没有实现。