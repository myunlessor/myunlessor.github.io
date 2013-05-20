---
layout: post
title: "使用Photoshop: 将整图一分为九"
date: 2013-05-20 20:31
comments: true
categories: [pragmatic, photoshop, javascript]
---

##引子##

前些天一同事在做拼图游戏。设计师提供了很多素材图片给他，这些图片都是整张整张的，他需要将这些图片切图成九宫格(3 x 3)、十六宫格(4 x 4)、二十五宫格(5 x 5)等。如果单张单张地进行计算然后裁切肯定不现实，那样实在效率低下，然后他问我有没快捷方法可以帮助他。

<!-- more -->

##思路一(动作)##

我们切图一般都在`photoshop`中完成。以往我遇到这种大量的重复性工作时，我绝对不会坐以待毙，我会想方设法，不达目的绝不罢休。通常面对这种问题时，我首先想到的就是生成一个`action`(动作)，然后利用它批量完成。

该`action`(动作)的大致思路是将各宫格图片分散到不同的图层中，然后便可以通过菜单命令`File | Scripts | Export Layers to Files…`将图层一一导出为文件，具体如下：

  * 计算一张图片的三等分宽高，生成并保存选区
  * 将选区定位在图片左上角，然后通过菜单命令`Layer | New | Layer via Cut(Copy)`将该区域隔离到新的图层
  * 重新载入选区，移位选区至新的位置，执行第二步同样命令
  * 重复执行第三步，直到图片九等分分散在不同图层

但是，生成这样的动作不仅麻烦，而且也不甚高效，原因如下：

  * 需要为九宫格(3 x 3)、十六宫格(4 x 4)、二十五宫格(5 x 5)不同规格生成不同的动作
  * 其他原因忘了~^~…

于是这种思路只成为了一种念想，一闪即过。

##思路二(切片工具)##

然后有考虑利用`Divide Slice…`(划分切图)及`Slices from Guides`(辅助线自动生成切片)功能——一种传统古老的切图方式。然后通过菜单命令`File | Save for Web…`将各切片导出为图片。这种方式可行是可行，但事实是提供的图片不是很理想，宫格中有1个像素的透明`gutter`(间隙)。如果不考虑`gutter`(间隙)的话，九宫格切图只需四条均分辅助线，否则需要八条，这样就会导出很多垃圾图片——1像素宽或(和)1像素高的图。这样效果不是很理想(自许准理想主义者)，于是这种方法也不了了之了。

> 事实是，这种方法确实可行，考虑四条均分辅助线生成切片，最后可以生成个`action`(动作)对这些图片做最后的`sanitization`(“消毒处理”)，傻眼了当时…

##思路三(脚本)##

最后，不得不实施`Last Resort`(破釜沉舟之计)。我想到了脚本语言(事实是，原来我调侃同事用写段`Java`代码生成图片…^-^)，`photoshop`自带的脚本功能(支持`JavaScript`、`VBScript`、`AppleScript`三种脚本语言)做这类事可谓游刃有余，一段简短的代码就可以干净利落地解决它，代码如下：

{% include_code 划分切图脚本 divide_slice.js %}

用法很简单，只需下载这段脚本到本地，打开需要切分的图片，然后执行菜单命令`File | Scripts | Browse…`，在打开的弹出框中找到该脚本，双击执行即可。

如果要处理的图片很多的话，配合动作使用即可实现批处理。

##参考书目##

1. [Photoshop CS6 Scripting Guide](http://wwwimages.adobe.com/www.adobe.com/content/dam/Adobe/en/products/photoshop/pdfs/cs6/Photoshop-CS6-Scripting-Guide.pdf)
2. [Photoshop CS6 JavaScript Ref](http://wwwimages.adobe.com/www.adobe.com/content/dam/Adobe/en/products/photoshop/pdfs/cs6/Photoshop-CS6-JavaScript-Ref.pdf)