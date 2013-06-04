---
layout: post
title: "JavaScript异步代码排程策略"
date: 2013-06-04 19:06
comments: true
categories: [pragmatic, javascript]
---

##问题##

写JavaScript脚本代码经常需要用到计时器(`window.setTimeout`)功能，先看如下代码片段：

```js
// 先解析，但延时1000ms
setTimeout(function foo() {
  console.log('foo');
}, 1000);

// 后解析，但延时100ms
setTimeout(function bar() {
  console.log('bar');
}, 100);
```

<!-- more -->

将该代码片段拷贝进Chrome浏览器的控制台(`Console`)中执行，可以发现在控制台中是先打印`bar`字符串，后打印`foo`字符串，也即是先执行了`bar`函数，后执行了`foo`函数。假如我们要让代码执行完`foo`函数后再执行`bar`函数，不难想到如下方法：

```js
setTimeout(function foo() {
  console.log('foo');

  setTimeout(function bar() {
    console.log('bar');
  }, 100);
}, 1000);
```

在控制台中测试发现这确实达到了我们的预期结果，但这种嵌套结构实在不优雅。当嵌套层级多时，代码可读性会变得相当差，试看如下代码片段：

```js
var foo = function () {
  console.log('foo');
};

var muo = {
  x: 'baz',
  bar: function () {
    console.log(this.x);
  }
};

var yell = {x: 'boo'};

var bear = function (x, y) {
  console.log(x + y);
};

setTimeout(function () {
  foo();

  setTimeout(function () {
    muo.bar();

    setTimeout(function () {
      muo.bar.call(yell);

      setTimeout(function () {
        bear(10, 17);
      }, 1);
    }, 10);
  }, 100);
}, 1000);
```

相信没多少人喜欢读这种缺乏结构的代码。那么，有什么办法可以让上述代码变得优雅起来呢？这就涉及到异步代码排程的问题。

##策略##

在上述第一段代码中，`setTimeout`方法设定的延时在一定程度上可以看成是代码执行顺序的优先级，它打乱了先来后到的规则，延时短的比延时长的优先级高，在同一作用域内计时器代码执行的顺序与解析的顺序无关，这就产生了异步问题，可以类比为现实中的插队行为。我们这里要解决的就是这种异步排程问题，我们要确保先来后到的规则，先执行先被解析的代码，后执行后被解析的代码。

我们知道，在银行窗口办理业务时，我们得先取票排队，先取票的先为之服务，后取票的后服务。当然，这里只考虑只有一个窗口的情况。

类似的，要解决异步代码排程问题，我们可以把要执行的代码当成任务约束在队列中，先入队的先执行，后入队的后执行（即`FIFO`），且保证同一时间最多允许一个任务执行。基于以上分析，我们可以设计如下策略：

```js
var schedule = (function (self) {
  var paused = false, // 标记状态
      queue  = [];     // 队列

  // 入队
  self.join = function (fn, params) {
    params = params || {};
    var args = [].concat(params.args);

    queue.push(function (_) {
      _.pause();
      setTimeout(function () {
        fn.apply(params.context || null, args);
        _.resume();
      }, params.delay || 1);
    });

    return exec();
  };

  self.pause = function () {
    paused = true;  // 忙碌
    return this;
  };

  // ready and call next
  self.resume = function () {
    paused = false; // 空闲
    setTimeout(exec, 1);
    return this;
  };

  function exec() {
    if (!paused && queue.length) {
      queue.shift()(self);  // 出队
      if (!paused) self.resume();
    }
    return self;
  }

  return self;
}(schedule || {}));
```

有了以上设计的排程规则，我们可以将如上多嵌套代码优雅地表达为：

```js
var foo = function () {
  console.log('foo');
};

var muo = {
  x: 'baz',
  bar: function () {
    console.log(this.x);
  }
};

var yell = {x: 'boo'};

var bear = function (x, y) {
  console.log(x + y);
};

schedule
  .join(foo, {
    delay: 1000 // 延时
  })
  .join(muo.bar, {
    delay: 100,
    context: muo // this解析上下文
  })
  .join(muo.bar, {
    delay: 10,
    context: yell // this解析上下文
  })
  .join(bear, {
    delay: 1,
    args: [10, 17] // 为bear函数提供参数
  });
```

##参考

* [Secrets of the JavaScript Ninja](http://goo.gl/1A8ew)