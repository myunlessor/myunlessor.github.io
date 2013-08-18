---
layout: post
title: "淘宝前端之智勇大闯关第三季攻略"
date: 2013-08-15 22:42
comments: true
categories: [javascript]
---

今天在群里看到好多人都在玩这游戏，都玩得挺high，自己也点进链接玩了下，第一次玩这类游戏，觉得挺有意思的，遂记录下自己的玩法。

首先，[游戏链接](http://ued.campus.alibaba.com/quiz3/index.php)如下：

```
http://ued.campus.alibaba.com/quiz3/index.php
```

<!-- more -->

该游戏一共有6关。

##第一关 —— 突破，带锁的门##

F12键打开控制台，输入以下代码，密码显现，按不同顺序尝试密码即可通关。

```js
[].forEach.call(Array(11).join('-'), powder.blow.bind(powder));
```

##第二关 —— 激光，前进的方向##

该关主要调整id为ma和mb两挡板元素的位置和角度形成反射即可通关，在控制台输入以下代码即可：

```js
(function (doc) {
  var mas = doc.getElementById('ma').style,
      mbs = doc.getElementById('mb').style;

  mas.top = '550px';
  mas.webkitTransform = 'rotate(-82deg)';

  mbs.top = '430px';
  mbs.webkitTransform = 'rotate(172deg)';
}).call(this, document);
```

##第三关 —— 坐标，隐藏的线索##

初看这个场景，看到三个定位角块，嗯这是二维码，但是是空白的，审查元素得知它是个canvas元素，需要画图将该二维码补充完整，在控制台输入以下代码完成：

```js
(function (ctx) {
  [].filter.call(document.body.childNodes, function (node) {
    return node.nodeType === 8;
  })[0].data.trim().split(' ').forEach(function (params) {
    ctx.fillRect.apply(ctx, params.split(','));
  });
})(document.getElementById('qr-canvas').getContext('2d'));
```

##第四关 —— 图案，疯狂的猜测##

本关类似于看图识字的游戏，在文本框输入图片对应的关键字即可，主要有以下这些：

```
github
v
css sprite
stackoverflow
underscore
jade
ubuntu
php
less
wordpress
sublime text
w3
grunt
npm
```

##第五关 —— 寻找，无尽的房间##

这关看得云里来雾里去，最开始一直更改url中查询字符串room的值，提示你不要人肉。控制台叫你用jquery通关，尝试许久，总结如下方法，在控制台运行后直接通关：

```js
(function ($, loc) {
  var ready = false,
      message = $('#message').text(),
      t = query('t'),
      url = '';

  function query(param) {
    var match = RegExp('[?&]' + param + '=([^&]*)').exec(loc.href.split('#')[0]);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
  }

  (function yoda(next_room) {
    $.get(loc.href.split('?')[0], {
      t: t,
      room: next_room
    }, function (resp) {
      var msg = $('#message', resp).text(),
          nextRoom = $('#next-room', resp).text();

      console.log(message += msg);

      if (ready) {
        url += msg;
      } else if (msg === '/quiz3/i') {
        ready = !ready;
        url += msg;
      }

      if (nextRoom) {
        yoda(nextRoom);
      } else {
        var nextUrl = loc.protocol + '//' + loc.host + url;
        console.warn('点击进入下一关^_^: ' + nextUrl);
        setTimeout(function () { loc.href = nextUrl; }, 5000);
      }
    });
  })($('#next-room').text());
})(jQuery, location);
```

##第六关 —— 消除! 最后的任务##

这关没想到什么好办法，浏览js文件`http://ued.campus.alibaba.com/quiz3/assets/js/step5.js`看到里面有`window.location`，于是直接在控制台输入如下代码，顺利通关：

```js
var p = document.getElementById('page').getAttributeNode('data-p').nodeValue;
window.location = Base64.decode(p);
```



