---
layout: post
title: "触摸Sublime Text Plugins"
date: 2013-12-17 21:02
comments: true
categories: [sublime text, python, pragmatic]
---

在[Sublime Text Snippets实用技巧二则][pragmatic-snippets]一文中提到可以通过`Sublime Text`的`Snippets`功能快速在页面中插入图片占位符标签，本来在此基础上借助`Sublime Text`的`Plugins(插件)`功能进一步完善它。

<!-- more -->

引子
---------------------------

我们知道[placekitten]为我们提供了为我们提供了生成图片占位符的方案，比如当我们在页面中插入`src`设为`http://placekitten.com/300/240`的`img`标签时，返回一张`300 x 240`的猫咪图片如下：

![kitten: 300 x 240](http://placekitten.com/300/240)

同样，[placehold.it]也提供了类似的服务，比如在页页插入`src`设为`http://placehold.it/300x240`的`img`标签时，返回一张标有图片尺寸的原型图，如下所示：

![placehold: 300 x 240](http://placehold.it/300x240)

现在我想利用同一个`tab trigger`可以将[placekitten]和[placehold.it]整合到一起。也就是说当我们输入`kitten`时触发的第一个编辑点输入格式为`{width}/{height}`时，得到相应尺寸的猫咪图片，而当我们输入格式为`{width}x{height}`时，得到
标有图片尺寸的原型图。显然这涉及到逻辑判断，这时`Snippets`的正则功能已无能为力了，至少我没想到办法。

这时，`Sublime Text`提供给我们的插件功能就派上大用场了。

正文
---------------------------

我们在`Sublime Text`官网上可以了解到，在`Sublime Text`的早期版本中，作者原本打算将`Scheme`语言作为`Sublime Text`的插件开发语言，但考虑到`Scheme`语言方言多，使用人少且门槛高。后来调研后决定采用`Python`脚本语言作为插件开发语言，事后证明这一抉择是十分明智的，`Python`脚本语言易学易用，使用人群广泛，才有了如今`Sublime Text`插件开发活跃的生态圈。

有关`Sublime Text`的插件开发文档可参考[这里][reference-plugins]、[这里][extensibility-plugins]还有[这里][reference-api]，[官网论坛][sublime-text-forum]也是个很不错的学习交流的地方，在此就不多讲了。

本文要分享的是一个很简单的通过`tab`触发的插件，以整合[placekitten]和[placehold.it]服务，具体触发机制如下：

  1. 输入`pi`后按`tab`键触发[placehold.it]服务，触发后可交互性指定图片占位符宽高了
  2. 输入`pi{numbers}`后按`tab`键触发[placehold.it]服务，其中`{numbers}`为图片占位符的宽高（即占位符图片为正方形）
  3. 输入`pi{width}x{height}`后按`tab`键触发[placehold.it]服务，其中`{width}`指定图片占位符的宽度，`{height}`指定图片占位符的高度，注意`{width}`和`{height}`之间是小写的`x`
  4. 输入`pi{width}X{height}`后按`tab`键触发[placekitten]服务，其中`{width}`指定图片占位符的宽度，`{height}`指定图片占位符的高度，注意`{width}`和`{height}`之间是大写的`X`

具体例子如下：

在文档中输入`pi`后按`tab`键触发后返回如下标签，此时高亮显示`300x240`，可以交互性地指定宽高了，然后`tab`键跳至第2个编辑点可选择是否保留`width`和`height`属性

```html
<img src="http://placehold.it/300x240" width="300" height="240" title="PLACE.IT: [300 x 240]" alt="" />
```

在文档中输入`pi100`后按`tab`键触发后返回如下标签，同时可选择是否保留`width`和`height`属性

```html
<img src="http://placehold.it/100x100" width="100" height="100" title="PLACE.IT: [100 x 100]" alt="" />
```

在文档中输入`pi150x180`后按`tab`键触发后返回如下标签，同时可选择是否保留`width`和`height`属性

```html
<img src="http://placehold.it/150x180" width="150" height="180" title="PLACE.IT: [150 x 180]" alt="" />
```

在文档中输入`pi150X180`后按`tab`键触发后返回如下标签，同时可选择是否保留`width`和`height`属性

```html
<img src="http://placekitten.com/150/180" width="150" height="180" title="KITTEN: [150 x 180]" alt="" />
```

废话不多说，最后附上相关代码：

{% include_code 图片占位符插件 PlaceImage.py %}

将此段代码直接保存到`Packages`目录下即可使用啦！

参考
---------------------------
1. [Plugins Reference][reference-plugins]
2. [Plugins Usage][extensibility-plugins]
3. [API Reference][reference-api]

[reference-plugins]: http://docs.sublimetext.info/en/latest/reference/plugins.html
[extensibility-plugins]: http://docs.sublimetext.info/en/latest/extensibility/plugins.html
[reference-api]: http://www.sublimetext.com/docs/3/api_reference.html
[sublime-text-forum]: http://www.sublimetext.com/forum/
[placekitten]: http://placekitten.com/
[placehold.it]: http://placehold.it/

[pragmatic-snippets]: /blog/2013/12/16/pragmatic-sublime-text-snippets/
