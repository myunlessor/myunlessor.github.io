---
layout: post
title: "利用Promise消除“先发起请求后收到响应”问题带来的副作用"
date: 2015-12-19 20:39
comments: true
categories: [javascript, pragmatic, promise]
---

## 问题分析

考虑这种应用场景：用户与页面进行交互，切换不同的查询条件，实时发起异步请求，待响应返回后，将响应数据渲染到页面指定区域。大部分情况下，前一次操作发起的请求都会比后一次操作发起的请求先响应。先响应的先渲染，后响应的将先渲染的结果覆盖。于是我们可以得到查询条件与响应数据显示一致的结果。这是我们所期望的结果，也是我们眼中的“正常”流程。如果我们认真对待它的话，是不应该忽略“异常”流程的。由于请求是异步的，前一次发起的请求不会阻塞后一次请求的发起，顺理成章地，前一次请求也未必会比后一次请求先返回。于是导致的直接后果就是后一次请求响应的数据先渲染，待前一次请求响应时，直接覆盖了后一次请求的渲染结果。这可不是我们所期望看到的。

<!-- more -->

以上场景如果用代码来描述的话，是这样的：

```javascript
var result;

// A function to simulate async request delay
var request = function (msec, mockedData, callback) {
  setTimeout(function () {
    callback(mockedData);
  }, msec);
};

var sample = [
  { msec: 200, data: 'stale' },
  { msec: 100, data: 'fresh' }
];

// 模拟`先发起请求后响应`的情景
sample.forEach(function (item) {
  request(item.msec, item.data, function (resp) {
    result = resp;
  });
});

// wait 1s, we inspect the `result`
setTimeout(function () {
  // we expect `result` to be `fresh`, but it is `stale`
  console.log(result); // => `stale`
}, 1000);
```

## 解决问题

解决方法有很多，归根结底我们需要解决的问题就是：在后一次请求响应返回并渲染时，保证渲染结果不会被前一次请求的响应结果覆盖。

### 简单粗暴式

最简单粗暴的方式就是在当前请求还未响应时，禁止发起下一次请求。对于性急的人来说，这种做法实在不可接受，直接pass。

### 简单直观式

另外一种思路：在每次响应后且在渲染之前，判断当前响应是不是对应最新一次请求的。是，则渲染；不是，则不渲染。

这种思路最容易想到的实现就是使用`全局变量`标记最新请求，`局部变量`标记当前请求，然后在响应回调中判断`局部变量`的值是否和`全局变量`的值一样。如果不一样，忽略响应结果；如果一样，我们可以断言这是最新请求的响应，直接渲染。

以下是这种思路针对上面代码的改写：

```javascript
var result;
var globalMark = 0;

// A function to simulate async request delay
var request = function (msec, mockedData, callback) {
  setTimeout(function () {
    callback(mockedData);
  }, msec);
};

var sample = [
  { msec: 200, data: 'stale' },
  { msec: 100, data: 'fresh' }
];

// 模拟`先发起请求后响应`的情景
sample.forEach(function (item) {
  var localMark = ++globalMark;

  request(item.msec, item.data, function (resp) {
    if (localMark !== globalMark) {
      return;
    }

    result = resp;
  });
});

// wait 1s, we inspect `result`
setTimeout(function () {
  // now our `result` is `fresh`, just as expected
  console.log(result); // => `fresh`
}, 1000);
```

和我们所期望的一样，这种思路可以正常工作，而且简单直观。但是当我们要处理大量这类请求问题时，这类重复逻辑的代码将散落在各个地方，不是很优雅。问题不在于思路上，而在于实现。我们需要在源头（请求）处规避（控制）问题，而不是到结果（响应）处解决问题。

### Promise式

`Promise`正在已经成为解决异步问题的一大解决工具了，经过多年的实际考验，它甚至已纳入W3C规范，制定标准API了。所以回到这个问题，`we should think in promise at the first place`。

例如，上面的`request`方法我们实际可以写成`Promise`的形式：

```javascript
// A function to simulate async request delay
var request = function (msec, mockedData) {
  return $.Deferred(function (dfd) {
    setTimeout(function () {
      dfd.resolve(mockedData);
    }, msec);
  }).promise();
};

request(200, 'some data').then(function (resp) {
  console.log(resp); // => 'some data'
});
```

我们可以封装出`promisify`方法，这样可以将形如`request`的方法方便地包装为`promise化`的方法：

**promisify [jQuery.Deferred版本]**

```javascript
var promisify = function (fn) {
  // Is `fn` thenable?
  return fn.then ? fn : function () {
    var args = [].slice.call(arguments);

    return $.Deferred(function () {
      fn.apply(null, args.concat(this.resolve));
    }).promise();
  };
};
```

**promisify [ES6版本]**

```javascript
var promisify = function (fn) {
  // Is `fn` thenable?
  return fn.then ? fn : function () {
    var args = Array.from(arguments);
    return new Promise(resolve => void fn(...args.concat(resolve)));
  };
};
```

以下是将`request`方法`promise化`的例子：

```javascript
// A function to simulate async request delay
var request = function (msec, mockedData, callback) {
  setTimeout(function () {
    callback(mockedData);
  }, msec);
};

// decorate `request` with `promisify`
request = promisify(request);

request(200, 'some data').then(function (resp) {
  console.log(resp); // => 'some data'
});
```

但是，单单凭`promisify`并不能解决我们最初的问题，我们需进一步将之前的思路翻译为`promise式`的代码。为了不改变原有调用方式，我们可以对原有`promisify`后得到的方法再进行一层装饰。装饰后的方法仍是`promise化`的，这样对外调用完全是透明的。

以下是装饰器的实现方法，我将它命名为`mutePrior`, 意为`mute prior`：

**mutePrior [jQuery.Deferred版本]**

```javascript
var mutePrior = function (promisifiedFunc) {
  // 用于存储`promise`对象，从第2个位置开始存储
  var registry = [0];

  return function () {
    var promise = promisifiedFunc.apply(null, arguments);

    // 已发起的请求(promise)入队，可以看到新发起的请求(promise)始终位列数组末尾
    registry.push(promise);

    return $.Deferred(function (dfd) {
      var proxyCallbacks = ['resolve', 'reject'].map(function (action) {
        return function () {
          // 关键代码：截获原有响应结果，判断对应请求是否为最新一次请求
          if (registry.indexOf(promise) === registry.length - 1) {
            dfd[action].apply(dfd, [].slice.call(arguments));

            // 重置`registry`
            registry.length = 1;
          }
        };
      });

      // 添加代理回调
      promise.then.apply(promise, proxyCallbacks);
    }).promise();
  };
};
```

**mutePrior [ES6版本]**

```javascript
var mutePrior = function (promisifiedFunc) {
  var registry = [0];

  return function () {
    var promise = promisifiedFunc(...arguments);
    registry.push(promise);

    return new Promise(function (...actions) {
      var proxyCallbacks = actions.map(action => function (result) {
        if (registry.indexOf(promise) === registry.length - 1) {
          action(result);
          registry.length = 1;
        }
      });

      promise.then(...proxyCallbacks);
    });
  };
};
```

有了`mutePrior`，一切都变得很简单了，简单到纯粹的模式复用了。

```javascript
var result;

// A function to simulate async request delay
var request = function (msec, mockedData, callback) {
  setTimeout(function () {
    callback(mockedData);
  }, msec);
};

// decorate `request` with both `promisify` and `mutePrior`
request = mutePrior(promisify(request));

var sample = [
  { msec: 200, data: 'stale' },
  { msec: 100, data: 'fresh' }
];

// 模拟`先发起请求后响应`的情景
sample.forEach(function (item) {
  request(item.msec, item.data).then(function (resp) {
    result = resp;
  });
});

// wait 1s, we inspect `result`
setTimeout(function () {
  // now our `result` is `fresh`, just as expected
  console.log(result); // => `fresh`
}, 1000);
```