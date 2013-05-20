---
layout: post
title: "文件批处理那些事儿"
date: 2013-05-19 11:14
comments: true
categories: [pragmatic]
---

##引子##

在日常工作中我们无疑会碰到形形色色的针对文件操作的重复性工作，比如说批量复制、批量替换、批量重命名、批量删除文件或文件夹等的机械活。机械意味着我们不应该执拗于手工地去完成它们，我们需要**尽力**地从中摆脱出来。

之前做过批量重命名的活，在那之前经常用`Adobe Bridge`用于文件管理，知道其中就有个叫`Batch Rename`的工具。我很推荐使用它，但它有个缺点，只能针对文件进行重命名，对文件夹无效。但瑕不掩瑜，它真的很棒，能出色地完成我指定规则的重命名工作。

之后为了应对文件批操作，我写了个`文件批处理小工具`。我对这玩意的评价是，它只能处理很窄范围的特点需求，稍微来点需求变更，它便束手无策、黯然失色。顺便再吐嘈一句，我用了把牛刀干了件杀鸡的事。

<!--more-->

直到最近做了些很坑爹的事，我们一直给设计部的设计变更擦屁股这话就不提了。橙视圈十二生肖和十二星座两个应用被改版得几尽与原先版本脱节，数据已不由后台接口提供，得自己手活制造一大批json序列文件用于界面查询，算下来有接近3k个文件。开始重复地做复制、重命名文件、填充数据，依此反复，一下午时间弄完不到400个文件。

这样下去可不是办法，久闻shell命令名不虚传，稍试了下水，便惊叹shell的无底深渊，一些简单的命令便帮我完成了一些不简单的事。

##正题##

假如我有一个名叫`template.json`的json模板数据文件，文件内容如下：

```json
{
  "result": "0",
  "dataArea": {
    "content": ""
  }
}
```

我要生成一堆类似`a_0.json、a_1.json...d_4.json`这样的序列文件，同时文件都包含`template.json`的内容，手活的话我会先复制一堆`template.json`文件，然后一个个重命名得到期望的序列文件，这真的很累。可是若借助shell命令的魔力，简直不费吹灰之力。

我们都知道`cp`是拷贝文件命令，例如在终端下执行：

```bash
> cp template.json a_0.json
```

那么在`template.json`文件的所在目录下将得到一个名为`a_0.json`的文件，内容与`template.json`一模一样。

那么如何批量生成一堆这样的序列文件呢？这意味着我们要重复执行`cp`命令，但每次执行时上述例子中指定的目标文件（`a_0.json`）要相应改变，这跟每次传入不同参数调用相同函数很有些类似。`xargs`命令就是帮助你做这件事的，以下是对xargs命令的简短介绍：

>`xargs`命令被用来构造参数列表并调用其他命令(工具)，它从标准输入流（`standard input`）或管道(`pipes`)中读取以空格或换行分隔的东西，这些读取的东西可以被当作其所调用的命令的参数传入，执行该命令一次或多次。

可以看出，`xargs`命令其实不**干实事**，它旨在督导和帮助其他一些**干实事**的命令（比如`cp、mdkir、mv、rm`等）重复做事，从而让那些**干实事**的命令尽显其能，这正是`xargs`本身的价值所在。那么如何使用它呢？请看以下这个例子：

```bash
> echo a_1.json a_2.json | xargs -n 1 -I {} cp template.json {}
```

执行以上命令后，可以看到`template.json`文件的所在目录下多了两个名字分别为`a_1.json、a_2.json`的文件，并且内容也和`template.json`一模一样。

对以上命令的一些解释：

* `echo a_1.json a_2.json`表示`echo`两个以空格分隔的字符串到输出流
* `|`表示管道，可以理解为将前一命令的输出流重定向到下一命令的输入流中，这有些类似于将函数调用得到的值作为参数传入到别一函数中
* `xargs`中重复调用`cp`命令，选项`-n 1`表过每次调用时只使用一个参数，并且`-I {}`像声明参数名一样，`cp template.json {}`中的`{}`正是使用该参数的位置

其结果是`cp`命令被执行了两次，第一次将`a_1.json`替换`{}`被执行，第二次将`a_2.json`替换`{}`被执行，于是实现了两次复制操作。我说了这和函数调用没什么两样。

还是回到之前的问题，怎么批量生成序列文件呢？我们现在找到了批量执行`cp`命令的方法，现在的问题简化到如何生成序列字符串的问题。很简单，看如下例子:

```bash
> echo {1..10}
1 2 3 4 5 6 7 8 9 10

> echo {a..g}
a b c d e f g

> echo {a..d}_{1..4}.json
a_1.json a_2.json a_3.json a_4.json
b_1.json b_2.json b_3.json b_4.json
c_1.json c_2.json c_3.json c_4.json
d_1.json d_2.json d_3.json d_4.json
```

看到规律了吧？以下是在`template.json`文件所在目录的子目录`seqs`下生成序列文件的命令：

```bash
> mkdir -p seqs
> echo {a..d}_{1..4}.json | xargs -n 1 -I {} cp template.json seqs/{}
```

##一些小实践##

下面是我实践过的一些例子，大家可自行实践，方法跟上面所讲的大同小异。

###1.应用打包批处理###

假如终端当前工作子目录为`works`，在该目录下有如下结构：

```
works
  |__ source_files      [应用源文件放置目录]
  |   |__ riddle           [我爱猜谜语]
  |   |__ brain_twists     [脑筋急转弯]
  |   |__ train_tickets    [火车票查询]
  |
  |__ package_files     [应用打包放置目录]
  |
  |__ package_template  [打包模板结构文件目录]
      |__ draw
      |   |__ icon
      |   |__ poster
      |__ assets
          |__brolife    [应用放置根目录]
```

我们要将`source_files`目录下的所有应用打包放置在`package_files`目录下，可执行如下命令：

```bash
# 在应用打包目录下建立相应的应用文件夹
> ls source_files | xargs -n 1 -I {} mkdir -p package_files/{}

# 拷贝文件夹需要带上`-r`选项表示递归拷贝
> ls source_files | xargs -n 1 -I {} cp -r package_temptate/* package_files/{}

# 将应用拷贝至相应的`brolife`文件夹中
> ls source_files | xargs -n 1 -I {} cp -r source_files/{} package_files/{}/assets/brolife
```

###2.应用解包

应用解包即是将应用从各用的`brolife`文件夹中拷贝出至统一的路径，原理跟打包都差不多，时间关系不允罗列相应命令。

###3.过滤应用中的`.htm`文件
只拷贝出应用中的`.htm`文件，其他文件全部忽略，这项操作需要用到find命令，时间关系不允过多解释。下面是一个使用的小例子：

```bash
# 查找当前目录及其子目录下所有以`.htm`后缀结尾的所有文件
> find . -name "*.htm" -type f

# 查找`~myunlessor/Desktop/riddle`目录及其子目录下所有以`.jpg`或`.png`后缀结尾的文件
> find ~myunlessor/Desktop/riddle \( -name "*.jpg" -or -name "*.png" \) -type f
```

##小结##

从以上例子可以看到有了`xargs`命令及管道后，这些朴素的**干实事**的命令像脱胎换骨了一样，相当强大。千里之行，始于足下！

##附录##

以上所讲的文件批处理解决方案都依赖于*NIX环境的shell，但我们工作在windows平台上[^fn1]，说这些有什么意义呢？没关系，我们有[Cygwin][0]，它在windows平台下极力模拟Linux环境，让我们可以在windows下使用Linux的一些实用工具。它的标语是：

> Get that Linux feeling - on Windows!

猛击[这里][1]下载安装使用起来吧！

[0]: http://www.cygwin.com/
[1]: http://cygwin.com/setup.exe

[^fn1]: Windows平台下有PowerShell，没使用过，但我想它也应该很擅长做这类事吧！
