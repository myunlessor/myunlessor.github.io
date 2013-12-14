---
layout: post
title: "拥抱Sublime Text Snippets"
date: 2013-12-15 17:07
comments: true
categories: [sublime text]
---

用过`Sublime Text`很长一段时间，对它的`Snippets(片段)`功能却是情有独钟。

它的用法很简洁，在文档编辑点敲入定义的触发字符(`tabTrigger`)，然后按下`tab`键就可以输出预先定义的片段文字(`content`)。

<!-- more -->

介绍
---------------------------

片段是通过普通的XML格式文件进行定义的，文件扩展名为`sublime-snippet`，自定义的片段一般存放在`Packages/User/snippets`目录下。通过菜单命令`Tools | New Snippet...`进行创建，统一格式如下：

```xml
<snippet>
  <content><![CDATA[]]></content>
  <tabTrigger></tabTrigger>
  <scope></scope>
  <description></description>
</snippet>
```

`snippet`元素由以下4个元素构成：

  * `content`: 实际片段内容
  * `tabTrigger(可选)`: 通过TAB键触发的代码片段的简短字符串，未指定时可通过绑定键盘快捷键触发该片段
  * `scope(可选)`: 指定触发激活该片段的作用域，如`text.html`、`js.source`
  * `description(可选)`: `completions`补全提示时该片段的描述语

当在`snippet`元素中包含了这些信息后，`Sublime Text`就知道什么何时可以触发，是否触发及在哪触发这个片段了。

`content`中可以包含任意字符，包含的字符必须置于`<![CDATA[`及`]]>`之间，否则`Sublime Text`不知道如何解析它。

如果要输出符号`$`，则须转义为`\$`，因为符号`$`在`content`中有特殊作用，具体如下：

  * 定义`环境变量名(environment variables)`，如`$SELECTION`，更多定义的环境变量参见[这里][environment-variables]
  * 定义通过`tab`或`shift+tab`键进行编辑点位置跳转的`域(fields)`
    * 语法：`$1` .. `$n`
  * 定义`占位符(placeholder)`，即带默认值的`域(fields)`
    * 语法：`${1:占位符}` .. `${n:占位符}`
  * 定义正则替换，详细的语法定义参见[这里][substitutions]
    * 语法 `${var_name/regex/format_string/}`, `${var_name/regex/format_string/options}`

`content`中不能直接键入字符串`]]>`，如果片段要实际输入`]]>`，可以书写为`]]$NOT_DEFINED>`，这里的`$NOT_DEFINED`可以是任意未定义的环境变量，而未定义的环境变量解析为空字符串，因此可以达到输出`]]>`的目的。

用例
---------------------------

定义并保存以下片段到`Packages/User/snippets/conditional-html-tag.sublime-snippet`后，就可以在`html`文件中键入`condhtml`后按`tab`键触发`content`中定义的内容了。

```xml
<snippet>
  <content><![CDATA[
<!--[if lt IE 7]> <html class="ie6"> <![endif]-->
<!--[if IE 7]>    <html class="ie7"> <![endif]-->
<!--[if IE 8]>    <html class="ie8"> <![endif]-->
<!--[if IE 9]>    <html class="ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html class=""> <!--<![endif]-->
]]></content>
  <tabTrigger>condhtml</tabTrigger>
  <scope>text.html</scope>
</snippet>
```

更多实用技巧参见文章[Sublime Text Snippets实用技巧二则][pragmatic-snippets]。

参考
---------------------------
1. [Snippets Reference][reference-snippets]
2. [Snippets Usage][extensibility-snippets]


[reference-snippets]: http://docs.sublimetext.info/en/latest/reference/snippets.html
[extensibility-snippets]: http://docs.sublimetext.info/en/latest/extensibility/snippets.html
[environment-variables]: http://docs.sublimetext.info/en/latest/reference/snippets.html#environment-variables
[substitutions]: http://docs.sublimetext.info/en/latest/reference/snippets.html#substitutions

[pragmatic-snippets]: /blog/2013/12/16/pragmatic-sublime-text-snippets/
