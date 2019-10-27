# 环境

​	项目运行环境如下：

* 软件：Python>=3.6，PyTorch>=0.4.0&&!=1.1.0

* 依赖的包：numpy, scipy, opencv, yacs, tqdm

  环境参考如下：

  * numpy=1.16.2
  * opencv=3.4.1
  * pytorch=1.0.1
  * scipy=1.2.1
  * torchvision=0.2.2
  * tqdm=4.31.1
  * yacs=0.1.6
  * pyqt5=5.13.0			
  * pyqt5-tools=5.13.0.1.5
  * pyqtchart=5.13.0

* 操作系统： 建议在windows上配置，使用Anaconda3进行包管理
    * 其中， numpy包Anaconda3自带
            pytorch、torchvision、open建议在清华镜像网站https://mirrors.tuna.tsinghua.edu.cn/中下载
            scipy、tqdm在anaconda cloud 查找相应命令下载

#
提取图像和语义分割的内容在extract包里面，建议将自己的模块做成python package，

# 项目运行

​	项目主体main函数位于main.py中，运行该文件即可。
    测试用数据视频位于input中，双眼数据位于eyaData中，运行后项目会自动在视频所在目录下常见image文件夹，存储按帧分割的图片，分析结果存储在该文件夹下的results文件夹中。
	当前程序每100帧截取一张图片，平均每张图片分析2-3分钟，请耐心等待。