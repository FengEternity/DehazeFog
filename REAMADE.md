# ImageDehazeFog
何恺明博士《Single Image Haze Removal Using Dark Channel Prior》论文及代码复现
# ImageDehazeFog

    何恺明博士《Single Image Haze Removal Using Dark Channel Prior》论文及代码复现

# 暗通道先验去雾算法

    该算法是计算机视觉领域何恺明大佬于2009年提出的图像去雾经典算法，并获取当年CVPR最佳论文。论文题目为《Single Image Haze Removal Using Dark Channel Prior》。下图是大佬的百科简介，是真的厉害，值得我们大家学习。

    2003年5月，何恺明拿到保送清华的资格，是当年执信中学唯一保送上清华大学的学生；高考结果出炉以后，何恺明获得满分900分的成绩，成为当年广东省9位满分状元之一。
    2009年，何恺明成为首获计算机视觉领域三大国际会议之一CVPR“最佳论文奖”的中国学者。
    在2015年的ImageNet图像识别大赛中，何恺明和他的团队用“图像识别深度差残学习”系统，击败谷歌、英特尔、高通等业界团队，荣获第一。
    何恺明作为第一作者获得了CVPR 2009，CVPR 2016和ICCV 2017（Marr Prize）的最佳论文奖，并获得了ICCV 2017最佳学生论文奖。
    2018年，第31届计算机视觉和模式识别大会（Conference on Computer Vision and Pattern Recognition, CVPR）在美国盐湖城召开，何恺明获得本届大会的PAMI年轻学者奖。
        
![](https://img-blog.csdnimg.cn/0839ce4e3cbf4f53b35cd86063838435.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

## 1.算法原理

    言归正传，如果是图像处理或研究图像去雾领域的作者，建议大家认真阅读这篇英文原文，能在2009年提出该算法真的很惊艳。

## 引用及参考中文论文

    何涛, 等. 基于暗通道先验的单幅图像去雾新算法[J]. 计算机科学, 2021.
    王蓉, 等. 基于改进加权融合暗通道算法的图像去雾研究[J]. 浙江科技学院学报, 2021.
    图像去雾算法的原理、实现、效果（速度可实时）- 挚爱图像处理
    图像去雾之何凯明暗通道先验去雾算法原理及c++代码实现 - Do it !

## 英文原文

    https://ieeexplore.ieee.org/document/5567108
    Single Image Haze Removal Using Dark Channel Prior
    https://ieeexplore.ieee.org/document/5206515
    Single image haze removal using dark channel prior

![](https://img-blog.csdnimg.cn/3416dd0a435b410ba5ece4c90b2f2821.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

**暗通道先验（Dark Channel Prior, DCP）去雾算法 依赖大气散射模型进行去雾处理，通过对大量有雾图像和无雾图像进行观察总结，得到其中存在的一些映射关系，然后根据有雾图像的形成过程来进行逆运算，从而恢复清晰图像。**

![](https://img-blog.csdnimg.cn/e1bde38155b046828fb13ee0309fbb79.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

算法实现过程及原理如下，参考何恺明老师和何涛老师的论文。

### (1) 大气散射模型

    在计算机视觉和计算机图形学中，方程所描述的大气散射模型被广泛使用。参数解释如下：

    x是图像的空间坐标
    I(x)代表有雾图像（待去雾图像）
    J(x)代表无雾图像（待恢复图像）
    A代表全球大气光值
    t(x)代表透射率
    方程右边第一项为场景直接衰减项，第二项为环境光项。

![](https://img-blog.csdnimg.cn/acc445eff5a84c27a4026f1e9c505f44.png#pic_center)

### (2) 暗通道定义

    在绝大多数非天空的局部区域中，某些像素总会至少有一个颜色通道的值很低。对于一幅图像J(x)，其暗通道的数学定义表示如下：

![](https://img-blog.csdnimg.cn/46432e67aecb4d029689a0ce72212ecf.png#pic_center)

    其中，Ω(x)表示以x为中心的局部区域，上标c表示RGB三个通道。该公式的意义用代码表达也很简单，首先求出每个像素RGB分量中的最小值，存入一副和原始图像大小相同的灰度图中，然后再对这幅灰度图进行最小值滤波，滤波的半径由窗口大小决定。

### (3) 暗通道先验理论

    暗通道先验理论指出：对于非天空区域的无雾图像J(x)的暗通道趋于０，即：

![](https://img-blog.csdnimg.cn/4ee0c04294e84a30b265933bb41ff1af.png#pic_center)

    实际生活中造成暗原色中低通道值主要有三个因素：

    a) 汽车、建筑物和城市中玻璃窗户的阴影，或者是树叶、树与岩石等自然景观的投影；
    b) 色彩鲜艳的物体或表面，在RGB的三个通道中有些通道的值很低（比如绿色的草地／树／植物，红色或黄色的花朵／叶子，或者蓝色的水面）；
    c) 颜色较暗的物体或者表面，例如灰暗色的树干和石头。

    

![](https://img-blog.csdnimg.cn/b12dc4e35c6e4c26a16971b6051f8485.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)
    
    总之，自然景物中到处都是阴影或者彩色，这些景物的图像的暗原色总是很灰暗的，而有雾的图像较亮。因此，可以明显的看到暗通道先验理论的普遍性。



![](https://img-blog.csdnimg.cn/c56ed7ffb3ce462d899491c0c37f2dc3.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

### (4) 公式变形

    根据大气散射模型，将第一个公式稍作处理，变形为下式：

![](https://img-blog.csdnimg.cn/40090d06199343da95460bd1f8c5d178.png#pic_center)

    假设每一个窗口的透射率t(x)为常数，记为t’(x)，并且A值已给定，对式两边同时进行两次最小值运算，可得：

![](https://img-blog.csdnimg.cn/910ee44d94ab4fcbbfdb5a89c9da92d0.png#pic_center)

    其中，J(x)是要求的无雾图像，根据前述的暗通道先验理论可知：

![](https://img-blog.csdnimg.cn/e2c744f21b334fc6bd0e7a949d1280e4.png#pic_center)

    因此可推导出：

    
![](https://img-blog.csdnimg.cn/0d02d7f93b7e47ef8de9416726f235dc.png#pic_center)

### (5) 透射率计算

    将上式带入可得到透射率t’(x)的预估值，如下所示：

![](https://img-blog.csdnimg.cn/383f3b7436ed4f0f91c7c07c99c0b652.png#pic_center)

    现实生活中，即便晴空万里，空气中也会存在一些颗粒，在眺望远处的景物时，人们还是能感觉到雾的存在。另外，雾的存在让人们感受到景深，因此在去雾的同时有必要保留一定程度的雾。可以通过引入一个0到1之 间 的 因 子 w（一 般取0.95）对预估透射率进行修正，如式所示：

![](https://img-blog.csdnimg.cn/a8fb67d3051a4ab5a0aac526dbf4f4de.png#pic_center)

    以上的推导过程均假设大气光值A是已知的，在实际中，可以借助暗通道图从原始雾图中求取。具体步骤如下：

    先求取暗通道图，在暗通道图中按照亮度的大小提取最亮的前0.1%的像素
    在原始雾图I(x)中找对应位置上具有最高亮度的点的值，作为大气光值A
    此外，由于透射率t偏小时，会造成J偏大，恢复的无雾图像整体向白场过度，因此有必要对透射率设置一个下限值t0（一般取值为0.1），当t值小于t0 时，取t=t0。将以上求得的透射率和大气光值代入公式，最终整理得到图像的恢复公式如下：


![](https://img-blog.csdnimg.cn/79825f7520f045619b57b3cd78c04e81.png#pic_center)
    
    这就是暗通道先验去雾算法的原理过程，下面简单补充论文中的处理效果图。
![](https://img-blog.csdnimg.cn/2d9a115f05f24b38a9461dec2d2470bd.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

再次膜拜偶像，极力推荐大家阅读论文。
