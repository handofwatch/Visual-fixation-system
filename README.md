#项目介绍

​	伴随着人工智能卷土重来的热潮，机器学习，深度学习也在加速发展，其中一个较大的领域，就是计算机视觉。当今，基于深度学习的图像分类技术在不断成熟，而图像的目标识别和语义分割可以说是图片分类的升级版本，并且有了较为广泛的应用，如人脸识别等。

​	图片的分类是指通过使用已经训练好的模型识别出输入图片的特征，然后将图片归于具体的类别。但是，对于实际获得的图片，其中不仅仅只有一个物体，这时就需要我们对一张图片的多个物体进行分类和识别。在进行图片目标的识别和语义分割之前，首先需要通过训练让我们搭建的模型知道每个类别的重要特征，当输入图片的信息中包含了我们的模型已经知道的类别特征时，就能很快将图片目标识别出来。

​	本项目是基于PyTorch的图片语义分割项目。PyTorch是一个以Python为优先的深度学习框架，代码简洁直观，不仅能够实现强大的GPU加速，而且还支持动态神经网络。

​	项目依赖语义分析和场景解析数据集ADE20K，该数据集非常庞大，包含20210个训练和2000个测试图片，具有150个语义类的具有挑战性的场景。

​	本项目使用的模型为在ImageNet上训练的基础模型。该模型采用BGR形式的输入而不是pytorch的默认实现所使用的RGB形式，必要时将自动下载基本模型。本次使用的模型为UperNet101，其参数如下：

| 模型       | 多范围测试 | 平均IoU | 像素精度（%） | 总分  | 速度（fps） | 培训时间（小时） |
| ---------- | ---------- | ------- | ------------- | ----- | ----------- | ---------------- |
| UperNet101 | No         | 42.00   | 80.79         | 61.40 | 7.8         | 2.5*25=62.5      |
| UperNet101 | Yes        | 42.66   | 81.01         | 61.84 | 2.3         | 2.5*25=62.5      |

​	自动编码器是一种可以进行无监督学习的神经网络模型。一个完整的自动编码器主要由两部分组成，分别为用于核心特征提取的编码部分和可以实现数据重构的解码部分，即编码器和解码器。

​	自动编码器主要应用在两个方面：其一是数据去噪，其二是进行可视化降维。自动编码器还有一个功能，是生成数据。

​	本项目将模型分为编码器和解码器。编码器通常直接从分类网络进行修改，解码器包括最终卷积和上采样。

编码器：

- MobileNetV2dilated
- ResNet18dilated
- ResNet50dilated
- ResNet101dilated

解码器：

- C1 (1 convolution module)
- C1_deepsup (C1 + deep supervision trick)
- PPM (Pyramid Pooling Module, see [PSPNet](https://hszhao.github.io/projects/pspnet) paper for details.)
- PPM_deepsup (PPM + deep supervision trick)
- UPerNet (Pyramid Pooling + FPN head, see [UperNet](https://arxiv.org/abs/1807.10221) for details.)

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


# 项目运行

​	项目主体main函数位于main.py中，运行该文件即可。
    测试用数据视频位于input中，双眼数据位于eyaData中，运行后项目会自动在视频所在目录下常见image文件夹，存储按帧分割的图片，分析结果存储在该文件夹下的results文件夹中。
	当前程序每100帧截取一张图片，平均每张图片分析2-3分钟，请耐心等待。