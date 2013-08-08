---
layout: post
title: "Photoshop趣味用法：玩转QQ找茬游戏"
date: 2013-08-08 22:52
comments: true
categories: [pragmatic, photoshop]
---

##引子##

相信不少童鞋都玩过QQ找茬游戏，游戏规则很简单：在2～4人的房间里，随机几组图片，每组图片分2张，找出每组图片中5处不同的地方，在规定的时间内谁找的茬多算谁赢。玩这个游戏的第一感觉就是各种眼花缭乱，我接受自己没有火眼金睛这一事实，在每组图规定的时间能平均能找出3个茬算是幸运之至了（我运气一向很差，无论做什么）。这样下来战绩总是令人沮丧，胜率老是上不去。尽管这些都是虚的，但心里多有不甘，于是就想到了一种投机取巧的办法——让Photoshop来充当自己的眼睛，自己则当指挥^_^。

<!-- more -->

其实最初用这方法玩找茬游戏还是三年前的事情了，只是近两天不知怎的突然心血来潮，有心将它记录下来留作纪念已矣。

##正文##

原理呢其实挺简单，找茬嘛就是找两张图的差异，这可是Photoshop最擅长做的事情啦（这也是我想到用它的原因）。在游戏过程中用Photoshop找茬需要解决的关键问题是如何做到迅速地让茬茬尽收眼底，显然Photoshop的Action最能胜任此类事情了。

如果Problem是输入的话，那么输出则是Solution。

现在的Problem是:

{% img /images/muo_img/zhaocha/problem.jpg %}

而所谓的Solution的就是这样的(瞧，5茬尽收眼底！):

{% img /images/muo_img/zhaocha/solution.jpg %}

从Problem出发，可以看出原图大小即为游戏窗口大小(`800 x 600`)，Solution中的结果图大小为原图中单张茬茬图的大小(`381 x 286`)，我们要做的就是从原图到结果图中的转换。

首先需要建一张`381 x 286`大小的纯黑色图片（比如将其保存为x.png，如下图）作为结果图的容器然后在Photoshop中打开。

{% img /images/muo_img/zhaocha/x.png %}

Photoshop要想获取游戏窗口的截图，需要剪贴板作为中介，在`Windows`下按快捷键`Alt + Print Screen`将当前激活窗口（这里即为游戏窗口）拷贝至剪贴板，这时在Photoshop就可以按`Ctrl + V`或`F4`键将截图拷贝至图层。

第二步就是录制`Action`啦，一共分为8步，如下图:

{% img left /images/muo_img/zhaocha/zhaocha_action.png %}

  * 粘贴：将通过`Alt + Print Screen`快捷键截取的游戏窗口粘贴到打开的`x.png`图片中作为图层
  * 图层对位：移动图层的位置使左张茬图完全显示在画布中
  * 复制图层：`Ctrl + J`复制图层到新的图层
  * 全选：`Ctrl + A`选区选中整个画布
  * 右对齐新复制的图层
  * 取消选择：`Ctrl + D`取消选区
  * 设置新复制图层的叠加模式为`Difference`
  * 移位新复制图层使右张茬图与左张茬图重叠得到Solution所示效果

<p style="clear:both"></p>

动作准备好后，玩游戏就是机械运动了：
  * `Alt + Print Screen` 截取游戏窗口
  * 切换到Photoshop执行脚本
  * 点点点点点、然后换图继续执行第一步

当然为了方便可以为动作设置快捷键。

我的做法，响应文件`Revert`事件：通过菜单命令`File | Scripts | Script Event Manager…`打开`脚本事件管理`弹出框，如下图，按以下方式进行设置：

{% img /images/muo_img/zhaocha/script_events_manager_panel.png %}

  * 勾选`Enable Events to Run Scripts/Actions`
  * `Photoshop Event`下拉框选择`Add an Event…`添加自定义事件
  * 在打开的`Add an Event`弹出框中
    * `Event Name`文本框填入`Revert`
    * `Descriptive Label`文本框填入`Rvrt`
    * 点击`OK`按钮完成添加
  * `Photoshop Event`下拉框选择刚刚添加的`Event`事件
  * 选中单选框`Action`，然后选择之前刚录制的动作

这时候`Alt + Print Screen` + `F12`的`“REPL”`完成，一切妥妥的、一切都变得机械！

##尾声##

当我利用这投机取巧的办法再次投入战斗时，真是屡试不爽、所向披靡。一相比较，游戏里的辅助道具实在弱爆了。我并不认为我这种玩法叫开挂，作弊一说也算勉强的了，晓之以理的讲法叫扬长避短、不亦乐乎。尽管缺失了些游戏的趣味性，但心理上得到的满足感却更强，这就够了。游戏说白了就是图个开心，每个人从中汲取开心的因子不一罢了。同时这也算是我用Photoshop比较有趣味的一种玩法吧！

P.S.：行文着实仓促!

##参考##

1. [Photoshop Programming Guide](http://tinyurl.com/kwmfjj9)