---
layout: post
title: "import this 与恺撒密码"
date: 2013-06-04 20:56
comments: true
categories: [python, javascript]
---

学过`python`脚本语言的人都知道`python`中有一个叫`this`的模块（`module`）。该模块只做了件很简单的事，打印一段字符串，内容是有关python语言的一些禅语（也可以称它为`python`哲学）。

<!-- more -->

要显示它很简单，在`python`的`REPL`（`Read-Eval-Print Loop`）中键入`import this`，可以看到如下字符串:

```
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

我想，这个模块应该是`python`里最简单、也最特殊的模块罢！出于好奇，查看了下这个模块的源码，如下所示：

{% include_code python哲学 this.py %}

呈现在眼前的不是一段平淡无奇的print语句，而采用了恺撒密码算法（`Caesar cipher`）。以下内容摘自维基百科，详见[凯撒密码](http://goo.gl/n9Ldz):

> 在密码学中,恺撒密码(或称恺撒加密、恺撒变换、变换加密)是一种最简单且最广为人知的加密技术。它是一种替换加密的技 术,明文中的所有字母都在字母表上向后(或向前)按照一个固定数目进行偏移后被替换成密文。例如,当偏移量是3的时候,所有的字母A将被替换成 D,B变成E,以此类推。这个加密方法是以恺撒的名字命名的,当年恺撒曾用此方法与其将军们进行联系。<br>
恺撒密码通常被作为其他更复杂的加密方法中的一个步骤,例如维吉尼尔密码。恺撒密码还在现代的 ROT13系统中被应用。但是 和所有的利用字母表进行替换的加密技术一样,恺撒密码非常容易被破解,而且在实际应用中也无法保证通信安全。

可以看到，恺撒密码的原理很简单，对每个字母按照同一偏移量映射为别的字母，这样就完成了简单的加密。

看到`this`模块，我最大的感悟就是`python`语言优雅简洁的表达能力，我试过用`JavaScript`语言表达恺撒密码，实在为它感到汗颜。大概是因为`JavaScript`表达的废话太多，才催生了`CoffeeScript`这种比`JavaScript`更具表达力的语言吧。当然这得力于`CoffeeScript`大量借鉴`python、ruby`这种表达能力强的语言的语法才使然哩！

`this.py`中用到的取余运算符`%`有一个很值得学习的技巧，比如我们想让一个变量在某个上限和下限范围内递增或递减，我们一般会写这样的代码：

```js
(function () {
  var lower   = 10,
      upper   = 17,
      current = 14;

  // 单位递增
  function next() {
    if (current < upper) {
      current += 1;
    } else {
      current = lower;
    }
    return current;
  }

  // 单位递减
  function prev() {
    if (current > lower) {
      current -= 1;
    } else {
      current = upper;
    }
    return current;
  }

  console.log(next()); // current = 15
  console.log(next()); // current = 16
  console.log(next()); // current = 17
  console.log(next()); // current = 10
}());
```

利用取余运算符`%`，我们可以将如上代码简化为如下（注意此时没有了`if`条件语句）:

```js
function () {
  var lower   = 10,
      upper   = 17,
      dist    = upper - lower + 1,
      current = 14;

  function next() {
    return (current = lower + (current - lower + 1 + dist) % dist);
  }

  function prev() {
    return (current = lower + (current - lower - 1 + dist) % dist);
  }

  console.log(prev()); // current = 13
  console.log(prev()); // current = 12
  console.log(prev()); // current = 11
  console.log(prev()); // current = 10
  console.log(prev()); // current = 17
}());
```

