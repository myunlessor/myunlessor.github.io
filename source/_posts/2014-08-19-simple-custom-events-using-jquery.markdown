---
layout: post
title: "使用jQuery实现简单的自定义事件功能"
date: 2014-08-19 22:06
comments: true
categories: [javascript, jquery]
---

众所周知，页面元素的交互离不开javascript的事件模型，DOM元素对事件有原生的支持。而事件并不是javascript语言本身的固有功能，它是一种模式，通常被叫做`发布/订阅(publish/subscribe)`模式。这种模式可以很好地令代码解耦，寥寥数十行的javascript原生代码就可以实现简单的事件模型，但要实现复杂又易用的事件模型并不是件简单的事。而如果项目使用jQuery类库的话，我们可以在它实现的事件模型基础上做一定的封装，实现简单的自定义事件功能。

<!-- more -->

既然jQuery实现有事件模型，为什么我们还要另外再整一套呢？jQuery实现的事件方法(像`on、off、trigger`等)都是绑定在jQuery包装集对象上的，如果我们想为普通的字面对象或通过构造函数实例化的对象添加事件，显然jQuery提供的那套事件模型不能直接拿来用。如果我们细微地思考下就知道，对jQuery的事件模型稍加包装可以直接应用到普通对象上——jQuery包装集可以包装任意对象，包括字面对象及实例化对象等。

以下是使用jQuery实现的`发布/订阅(publish/subscribe)`模式。

##全局静态事件实现##

```js
!(function ($) {
  var o = $({});

  $.subscribe = function () {
    o.on.apply(o, arguments);
  };

  $.unsubscribe = function () {
    o.off.apply(o, arguments);
  };

  $.publish = function () {
    o.trigger.apply(o, arguments);
  };
})(jQuery);

// 使用
$.subscribe('howdy', function (e, data) {
  //=> ["one", "two"]
  console.log(data);
});

$.publish('howdy', [['one', 'two']]);
```

##适配一般对象的自定义事件实现##

```js
var pubsub = {
  _$: function () {
    return this.__$ || (this.__$ = $(this));
  },
  on: function () {
    return this._$().on.apply(this._$(), arguments)[0];
  },
  one: function () {
    return this._$().one.apply(this._$(), arguments)[0];
  },
  off: function () {
    return this._$().off.apply(this._$(), arguments)[0];
  },
  emit: function (events, data) {
    return this._$().trigger(events, [data])[0];
  }
};

// 使用

// =====================
// 字面对象添加自定义事件
// =====================
var obj = {};
$.extend(obj, pubsub);

obj
  .on({
    'hello': function (e, data) {
      //=> 'how are you today?'
      console.log(data);
    },
    'bye': function (e, data) {
      //=> 'good night!'
      console.log(data);
    }
  })
  .emit('hello', 'how are you today?')
  .emit('bye', 'good night!');

// =====================
// 实例化对象添加自定义事件
// =====================

// 构造函数
var Foo = function () {};

// 将事件方法添加到构造函数的原型上
$.extend(Foo.prototype, pubsub);

// 实例化对象
var foo = new Foo();

foo.on('howdy.with.namespace', function (e, data) {
  //=> { spam: "one", eggs: "two" }
  console.log(data);
});

foo.emit('howdy', { 'spam': 'one', 'eggs': 'two' });
```

通过以上代码我们可以看到，编写区区几行代码，我们就实现了适配一般对象的复杂易用的事件模型，它具有jQuery事件模型一切强大的功能。另外，我们注意到改造后的事件模型和Backbone实现的事件模型特别相似。另外，如果采用ES6环境，上述代码还可继续简化。

```js
var pubsub = {
  _$: function () {
    return this.__$ || (this.__$ = $(this));
  },
  on: function () {
    return this._$().on(...arguments)[0];
  },
  one: function () {
    return this._$().one(...arguments)[0];
  },
  off: function () {
    return this._$().off(...arguments)[0];
  },
  emit: function (events, data) {
    return this._$().trigger(events, [data])[0];
  }
};
```

END

