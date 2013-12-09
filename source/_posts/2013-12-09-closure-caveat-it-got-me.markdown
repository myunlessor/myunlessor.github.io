---
layout: post
title: "闭包陷阱：我中招了！"
date: 2013-12-09 21:37
comments: true
categories: [javascript]
---

一直以来我都以为自己对js的闭包功能掌握的还算可以，最近在工作中却实实在在地被闭包整了一回，特记录于斯，以为警戒！

<!-- more -->

以下代码是从工作中提炼出来的，在这4个case中两次调用`howdy()`函数时log打印值分别是什么？

```js
// closure caveat

// case 1
;(function (window, $, undefined) {
  var $target;

  function howdy() {
    var x = 'foo';

    if (!$target) {
      $target = $({})
        .on('whatever', function () {
          console.log(x);
        })
        .on('soga', function () {
          x = 'bar';
        });

      $target.triggerHandler('soga');
    }

    $target.triggerHandler('whatever');
  }

  howdy();
  howdy();
})(this, jQuery);

// case 2
;(function (window, $, undefined) {
  var $target, x;

  function howdy() {
    x = 'foo';

    if (!$target) {
      $target = $({})
        .on('whatever', function () {
          console.log(x);
        })
        .on('soga', function () {
          x = 'bar';
        });

      $target.triggerHandler('soga');
    }

    $target.triggerHandler('whatever');
  }

  howdy();
  howdy();
})(this, jQuery);

// case 3
;(function (window, $, undefined) {
  var $target;

  function howdy() {
    var x = 'foo';

    if (!$target) {
      $target = $({}).on('soga', function () {
        x = 'bar';
      });
    }

    $target
      .off('whatever')
      .on('whatever', function () {
        console.log(x);
      });

    $target.triggerHandler('soga');
    $target.triggerHandler('whatever');
  }

  howdy();
  howdy();
})(this, jQuery);

// case 4
;(function (window, $, undefined) {
  var $target, x;

  function howdy() {
    x = 'foo';

    if (!$target) {
      $target = $({}).on('soga', function () {
        x = 'bar';
      });
    }

    $target
      .off('whatever')
      .on('whatever', function () {
        console.log(x);
      });

    $target.triggerHandler('soga');
    $target.triggerHandler('whatever');
  }

  howdy();
  howdy();
})(this, jQuery);
```

总结：`prefer object properties to local variables when recording state!`
