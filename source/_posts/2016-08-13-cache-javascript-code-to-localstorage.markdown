---
layout: post
title: "缓存JS代码到本地localStorage的一种思路"
date: 2016-08-15 11:22
comments: true
categories: [javascript, pragmatic, localstorage]
---

为了加快页面的加载速度和交互速度，缓存JS脚本文件内容到本地`localStorage`（以下简称`缓存JS`）是一种行之有效的手段。

以加载`foo.js`文件为例，`缓存JS`的逻辑大致如下：

{% img /images/cachejs2localstorage/cache-to-local.png %}

<!-- more -->

在实际应用中，`缓存JS`需要解决以下两个问题：

- 获取JS脚本文件的内容并写入缓存
- JS脚本文件的内容变化时自动更新缓存

## 获取JS脚本文件的内容并写入缓存

前端JS文件一般使用单独的域名存放到CDN上，跨域问题使得我们无法通过ajax请求获取JS文件的内容。

那有其他办法可以获取脚本文件的内容吗？答案是有的。

以`https://www.xxx.com/static/js/foo.js`为例，其文件内容如下：

```js
console.log('first line');
console.log('second line');
```

大家都知道，函数是可以转换成字符串类型的，因此我们可以这种方式获取函数本身的代码，如下所示：

```js
function foo() {
  console.log('first line');
  console.log('second line');
}

// 函数转换为字符串 => 函数代码的字符串形式
console.log(String(foo));

// 也可以这样调用得到
console.log(foo.toString());
```

得到函数完整的字符串代码后，需要将字符串进行剥离，只获取得到body部分，这一步可以使用正则表达式将body匹配出来：

```js
// 正则表达式匹配完整的函数语句
// 这里使用`^`和`$`匹配头尾，匹配性能不成问题
var rfunc = /^function\s*(?:[^(]*)\(([^)]*)\)\s*{([\s\S]*)}$/;

// 变量`code`存放的就是`foo.js`的代码内容
var code = String(foo).match(rfunc) && RegExp.$2;
console.log(code);
```

所以，将原代码包裹一层`function`，我们可以成功拿到任意脚本文件的内容，而完全不用关心是否存在跨域问题。

于是我们可以将原先的`foo.js`自动转换成如下形式，这一步实际可以通过构建（打包）工具（如`webpack`）自动完成。

```js
// 自执行函数
void function (fn) {
  // 执行代码逻辑
  fn.call(function () { return this; }());

  var rfunc = /^function\s*(?:[^(]*)\(([^)]*)\)\s*{([\s\S]*)}$/;
  var code = String(fn).match(rfunc) && RegExp.$2;

  // TODO: 将`code`写入到`localStorage`中（见下文）
}(function () {
  console.log('first line');
  console.log('second line');
});
```

## JS脚本文件的内容变化时自动更新缓存

我们可以通过计算文件内容的md5值，然后取md5值前面若干位作为文件的版本号拼到文件名中（如`foo.09c1ff3231.js`、`foo.b9193b0ded.js`等），以此标记文件内容发生了变化。

假设`foo.09c1ff3231.js`是旧版本文件，`foo.b9193b0ded.js`是新版本文件，用流程图可以清晰地呈现缓存自动更新的过程：

{% img /images/cachejs2localstorage/update-cache-to-local.png %}

## 实际应用

在实际应用中，我们可以将缓存相关的逻辑封装到普通对象（如命名为`StoreManager`，并保存为文件`store-manager.js`，该对象应实现如下几个功能：

- 获取指定脚本文件名的缓存内容
- 判断是否已缓存指定版本号的文件内容
- 将指定版本号的文件内容写入到缓存（或替换掉已缓存版本）
- 将指定脚本文件名的内容从缓存中移除
- 清理已过期的缓存内容（可选）

以下是`StoreManager`的实现代码：

```js
void function (global) {
  var storage = global.localStorage;

  // 缓存js时存储的key使用统一的前缀作为命名空间
  // 这样方便管理及尽可能避免冲突
  var prefix = 'store-manager/js/';

  // 匹配版本号(8~12位)
  var rkey = /^(.+)\.(\w{8,20})\.js$/;

  // 默认缓存时长
  // 30 days (单位：小时)
  var defaultExpiration = 30 * 24;

  var store = {
    // 获取指定脚本文件名的缓存内容
    get: function (key) {
      var item = storage.getItem(prefix + key);
      try {
        return JSON.parse(item || 'false');
      } catch (e) {
        return false;
      }
    },

    // 判断是否已缓存指定版本号的文件内容
    has: function (md5key) {
      var matches = String(md5key).match(rkey);
      return matches ? (this.get(matches[1]).md5 === matches[2]) : false;
    },

    // 将指定版本号的文件内容写入到缓存（或替换掉已缓存版本）
    set: function (md5key, code, opts) {
      var matches = String(md5key).match(rkey);

      if (matches) {
        var now = +new Date;
        var storeKey = prefix + matches[1];

        opts || (opts = {});

        var storeVal = {
          'md5': matches[2],
          'stamp': now,
          'expire': (now + (opts.expire || defaultExpiration) * 60 * 60 * 1000),
          'code': code,
        };

        storage.setItem(storeKey, JSON.stringify(storeVal));
      }

      return this;
    },

    // 将指定脚本文件名的内容从缓存中移除
    remove: function (key) {
      storage.removeItem(prefix + key);
      return this;
    },

    // 清理（已过期的）缓存内容
    clear: function (expired) {
      var now = +new Date;

      for (var item in storage) {
        var key = item.replace(prefix, '');

        if (key && (!expired || this.get(key).expire <= now)) {
          this.remove(key);
        }
      }

      return this;
    },
  };

  // 导出为全局变量
  // 注：一旦我们的脚本重命名后，缓存的旧版本会失去跟踪，
  // 执行`clear(true)`，这样失去跟踪的缓存内容过期后能够得到清理
  global.StoreManager = store.clear(true);

}(function () { return this; }());
```

有了`StoreManager`对象后，我们就可以轻松地`缓存JS`了。

- 源文件`foo.js`：

```js
console.log('line 1');
console.log('line 2');
```

- 通过构建（打包）工具得到`foo.b9193b0ded.js`(这里md5随便取的名，实际代码应该需要精简)：

```
// 自执行函数
void function (fn) {
  // 执行代码逻辑
  fn.call(function () { return this; }());

  // 容错检测
  if (typeof StoreManager === 'object' && StoreManager) {
    var rfunc = /^function\s*(?:[^(]*)\(([^)]*)\)\s*{([\s\S]*)}$/;
    var code = String(fn).match(rfunc) && RegExp.$2;

    if (code) {
      // 缓存一个月
      StoreManager.set('foo.b9193b0ded.js', code, { 'expire': 720 });
    }
  }
}(function () {
  console.log('line 1');
  console.log('line 2');
});
```

- 得到条件判断加载（执行）`foo.b9193b0ded.js`文件的代码（同上，实际代码应该需要精简）：

```html
<!-- 预先引入`store-manager.js` -->
<script src="https://www.xxx.com/static/js/store-manager.js"></script>

<!-- 或者将`store-manager.js`内联到页面中 -->
<script> /* 精简过的`store-manager.js`代码 */ </script>

<!-- 通过构建（打包）工具得到如下<script>片段 -->
<script>
if (typeof StoreManager === 'object' && StoreManager && StoreManager.has('foo.b9193b0ded.js')) {
  try { eval(StoreManager.get('foo').code); }
  catch (e) {}
} else {
  document.write('<script src="https://www.xxx.com/static/js/foo.b9193b0ded.js"><\/script>');
}
</script>

<!-- 其他需缓存的js脚本文件，etc -->
<script>
if (typeof StoreManager === 'object' && StoreManager && StoreManager.has('bar.3e9a1fbe8c.js')) {
  try { eval(StoreManager.get('bar').code); }
  catch (e) {}
} else {
  document.write('<script src="https://www.xxx.com/static/js/bar.3e9a1fbe8c.js"><\/script>');
}
</script>
```

最后，`localStorage`针对每个域可存储容量很有限，需节制使用。