---
layout: post
title: "Sublime Text Snippets实用技巧二则"
date: 2013-12-16 18:22
comments: true
categories: [sublime text, pragmatic]
---

由于`Sublime Text Snippets`功能设计的强大和灵活性（TAB跳转、多编辑点多选区支持、正则匹配替换等），我们可以很方便地将它应用到各种能用上它的场合。

关于`Sublime Text Snippets`的基本介绍可参见文章[拥抱Sublime Text Snippets][embrace-snippets]以及该文章给出的参考文档。

下面列举使用`snippet`的实用技巧，参详这两例子后，大可举一反三而为之。

<!-- more -->

一、选区片段包裹
---------------

现在前端开发环境少不了模板系统的使用，诣如[Mustache][mustache]、[Handlebars][handlebars]、[Underscore][underscore.template]和[Lo-Dash][lodash.template]等。

模板系统一般都在模板上下文中内嵌`分隔符(delimiter)`进行解析，像[Underscore][underscore.template]和[Lo-Dash][lodash.template]默认有`<%  %>(interpolate delimiter)`、`<%=  %>(evaluate delimiter)`及`<%-  %>(escape delimiter)`，使用模板的时间书写这些分隔符尤显得不太方便。借助`Sublime Text Snippets`可以使书写模板不再头痛。

下面这个`snippet`我将它保存为`Packages/User/snippets/angle-delimiter.sublime-snippet`，你会注意到元素`snippet`中只包含`content`一个元素，在`content`中定义了两个跳转`编辑点(edit point)`，同时将环境变量`$SELECTION(文本选区)`作为`编辑点2($2)`的占位符。

```xml
<snippet>
  <content><![CDATA[
<%$1 ${2:$SELECTION} %>
]]></content>
</snippet>
```

这样当我们选中文本(可以为空，单个或多个选区)后，触发该片段后就可以将选中文本包裹在`<%`和`%>`间，同时跳转到`编辑点1($1)`，可以选择性地添加`=`或`-`从而定义不同的`分隔符(delimiter)`。但是我并没有定义`tabTrigger`元素进行`tab`触发，原因是我们这里包含环境变量`$SELECTION(文本选区)`，使用`tabTrigger`无法达到片段包裹的目的，因此我们选择定义键盘快捷键来触发该片段，如下所示：

```json
{
  "keys": ["super+k", "super+5"],
  "command": "insert_snippet",
  "args": {
    "name": "Packages/User/snippets/angle-delimiter.sublime-snippet"
  }
}
```

将此段代码加入到`Packages/User/Default (OSX).sublime-keymap`后，然后选中你想包裹的文本，此时先后按下快捷键`cmd + k`、及`cmd + 5`后可以触发该片段。Cool!


二、正则匹配替换
---------------

有时候我们进行页面重构的时候，需要使用占位图片进行临时布局。[placekitten][placekitten]提供了一个快速而简单的服务帮我们完成此目的。

比如我们需要在页面某个位置放置一个宽200高300的图片，只需要添加如下标签代码即可，如下所示：

```html
<img src="http://placekitten.com/200/300" width="200" height="300" title="KITTEN: [200 x 300]" alt="" />
```

然后`placekitten`会给我们返回一张`200 x 300`的猫咪图片，我们只要指定任意宽高就好了，so cutely it is!

使用`Sublime Text Snippets`提供的正则区配替换特性，我们可以快速输出以上标签，使得图片占位更加称心如意。片段如下：

```xml
<snippet>
  <content><![CDATA[
<img src="http://placekitten.com/${1:300/240}"${2: width="${1/^\/?([^\/]+)\/?.*$/$1/}" height="${1/^([^\/]*?)\/?([^\/]+)\/?$/$2/}"} title="KITTEN: [${1/^\/?([^\/]+)\/?.*$/$1/} x ${1/^([^\/]*?)\/?([^\/]+)\/?$/$2/}]" alt="" />
]]></content>
  <tabTrigger>kitten</tabTrigger>
  <scope>text.html</scope>
</snippet>
```

将此片段保存到`Packages/User/snippets/placekitten.sublime-snippet`，然后在我们的html页面中敲入`kitten`后按`tab`键，输出标签如下：

```html
<img src="http://placekitten.com/300/240" width="300" height="240" title="KITTEN: [300 x 240]" alt="" />
```

此时`300/240`处于高亮显示，这是我们的第一个编辑点，在这个编辑点我们可以随意更改宽高值，可以看到`width`、`height`及`title`三个标签属性值跟着变化。

比如替换为`250`，标签显示为：

```html
<img src="http://placekitten.com/250" width="250" height="250" title="KITTEN: [250 x 250]" alt="" />
```

替换为`400/300`，标签显示为：

```html
<img src="http://placekitten.com/400/300" width="400" height="300" title="KITTEN: [400 x 300]" alt="" />
```

如果我们不需要` width="xxx" height="xxx"`，这里按`tab`跳至第二个编辑点，按`delete`键即可删除，awesome!


[mustache]: https://github.com/janl/mustache.js
[handlebars]: http://handlebarsjs.com/
[underscore.template]: http://underscorejs.org/#template
[lodash.template]: http://lodash.com/docs#template
[placekitten]: http://placekitten.com/

[embrace-snippets]: /blog/2013/12/15/embrace-sublime-text-snippets/
