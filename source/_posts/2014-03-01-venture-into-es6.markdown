---
layout: post
title: "浅尝ECMAScript 6"
date: 2014-03-01 10:43
comments: true
categories: [javascript]
---

现在ECMAScript 6草案制定在不断地推进，浏览器们也在跟进实现，了解ES6的提供的诸多特性是势在必行的事了。

有关浏览器们对ECMAScript 6草案的实现情况可参阅[这里](http://kangax.github.io/es5-compat-table/es6/)。

有关ES6的语言特性可参阅[这里](https://github.com/google/traceur-compiler/wiki/LanguageFeatures)。

目前对ES6实现较为充分的环境有[Google Traceur Compiler](https://github.com/google/traceur-compiler)及[Firefox Nightly](http://nightly.mozilla.org/)。

有关`traceur compiler`的环境配置如下：

```html
<script src="https://traceur-compiler.googlecode.com/git/bin/traceur.js"></script>
<script src="https://traceur-compiler.googlecode.com/git/src/bootstrap.js"></script>
<script>
traceur.options.experimental = true;
</script>
<script>
  // blablabla...
</script>
```

<!-- more -->

I、新的语法
----------------------------------------------------

###1. 块作用域(Block Scope)

`var`关键字声明的变量具有函数作用域或全局作用域，而通过`let`关键字将变量声明为块作用域，对比如下：

```js
// 在块(curly)作用域中声明并初始化变量
{ var foo = 'foo'; }
{ let bar = 'bar'; }

console.log(foo); // -> 'foo'
console.log(bar); // ReferenceError: bar is not defined
```

###2. 常量(Constants)

许多语言都有常量的概念(值不能改变的变量)。ES6草案将常量引入到了JavaScript中。

使用`const`关键字将变量声明为常量，规范要求`const`声明的常量具块作用域，某些浏览器目前将其实现为函数作用域或全局作用域。声明变量为常量时如果不赋值，某些浏览器会将该变量赋`undefined`值，而某些浏览器则直接报错。为常量重新赋值，某些浏览器会忽略新赋值，某些浏览器会报错。将引用类型（如数组或对象）声明为常量，并不影响引用类型的扩充行为：

```js
const noexist;             // Const must be initialized (IE)
const foo = 'foo';
foo = 'hoo';               // Assignment to const (IE)
console.log(foo);          // -> 'foo'

// 常量引用类型并不影响对其自身的扩充(`augument`)
const bar = [];
bar.push('spam', 'eggs');
console.log(bar.length);   // -> 2

// 同上
const baz = {};
baz.spam = 'eggs';
console.log(baz.spam);     // -> 'eggs'
```

###3. 默认参数(Default Parameters)

函数声明时可以为参数赋予默认值，这样函数调用时如果参数缺省(`undefined`)，则该参数会被赋予默认值，使用默认参数在一定程序上使函数声明更为直观，并且简化我们的代码。

```js
// 传统写法
function fill(container, liquid) {
  if (typeof liquid === 'undefined') {
    liquid = 'coffee';
  }
  // blablabla...
}

// 新式写法
function fill(container, liquid = 'coffee') {
  // blablabla...
}
```

###4. Rest和Spread操作符

很多时候我们处理函数的时候需要用到数组参数，ES6提供的`Rest`和`Spread`操作符可以让我们更方便地处理数组参数。

`rest`是将多值折叠为单值集合的过程，和`rest`相反，`spread`是将单值集合展开为多值的过程。很多语言都有对它的支持，语法略有差异，Python、Ruby和CoffeeScript将这种语法统称为`splats`，Python和Ruby用形如`*var`的语法来表达。CoffeeScript用形如`var...`的语法来表达，而ES6则用形如`...var`的语法来表达。


```js
// 1. rest
function unary(...first) {
  console.log(first);
}

function binary(first, ...rest) {
  console.log([first, rest]);
}

unary('foo');                 // -> ['foo']
unary('foo', 'bar');          // -> ['foo', 'bar']

binary('foo');                // -> ['foo', []]
binary('foo', 'bar', 'baz');  // -> ['foo', ['bar', 'baz']]

// rest实现
;(function (window, undefined) {
  var _slice = Array.prototype.slice;

  function variadic(fn) {
    var numParams    = fn.length, // 形参个数
        numNamedArgs = numParams - 1;


    return numParams < 1 ? fn : function () {
      var
        numArgs             = arguments.length, // 实参个数
        namedArgs           = _slice.call(arguments, 0, numNamedArgs),
        numMissingNamedArgs = Math.max(0, numNamedArgs - numArgs),
        argPadding          = Array(numMissingNamedArgs),
        variadicArgs        = _slice.call(arguments, numNamedArgs);

      return fn.apply(this, namedArgs
                              .concat(argPadding)
                              .concat([variadicArgs]));
    };
  }

  window.variadic = variadic;
}).call(this, this);

// -> ['why', 'hello', 'there']
variadic(unary)('why', 'hello', 'there');

// -> ['why', ['hello', 'there']]
variadic(binary)('why', 'hello', 'there');

// ----------------------------------------------------

// 2. spread
var numbers = [1, 2, 3, 4, 5];

// 传统写法
var max = Math.max.apply(Math, number);

var filled = numbers.slice(0);
[].push.apply(filled, [6, 7, 8, 9, 10]);

// 新式写法
var max = Math.max(...number);
var filled = [...numbers, 6, 7, 8, 9, 10]
```

###5. 解构赋值(Destructuring Assignment)

如果你想从数组中拿取多个元素并赋予其他变量，或是从函数中返回多值，那么ES6提供的`解构赋值(Destructuring Assignment)`特性正是我们所需要的。

```js
// 1. 数组解构赋值
let a = 1, b = 2;
[b, a] = [a, b];   // swap two variabls

console.log(a, b); // -> 2 1

function dest() {
  return ['why', 'hello', 'there'];
}

let [foo, bar, baz] = dest();

// -> 'why' 'hello' 'there'
console.log(foo, bar, baz);

// 忽略不需要的值
let [a, , c] = dest();

// -> 'why' 'there'
console.log(a, c);

// 2. 对象解构赋值
let janeDoe = {
  first: 'jane',
  last: 'doe',
  gender: 'female',
  hobbies: ['music', 'sports']
};

let { first: firstName, last: lastName } = janeDoe;

// -> 'jane' 'doe'
console.log(firstName, lastName);

let { first, last } = janeDoe;

// -> 'jane' 'doe'
console.log(first, last);

function whatever({ first: f, last: l }) {
  console.log(f, l);
}

// -> 'jane' 'doe'
whatever(janeDoe);

function another({ gender, hobbies: [hob1, hob2] }) {
  console.log(gender, hob1, hob2);
}

// -> 'female' 'music' 'sports'
another(janeDoe);
```

###6. for…of 循环语句

ES6新引入了`for…of`循环语句，以往我们使用的`for..in`循环语句用于迭代对象的`属性(properties)`，而新式的for…of循环语句则用于迭代对象的`值(values)`。

```js
var numbers = [1, 2, 3, 4, 5];

// 传统写法
numbers.forEach(function (number) {
  console.log(number);
});

// 新式写法
for (let number of numbers) {
  console.log(number);
}
```

###7. 迭代器(Iterators)

`for..of`循环只对迭代对象有效，这意味着要使一个对象可迭代，对象自身需要迭代器。具体可移步参阅[这里](https://github.com/google/traceur-compiler/wiki/LanguageFeatures#wiki-iterators-and-for-of-loops)

###8. 生成器(Generators)

生成器可以创建迭代器，并且可以用它来创建自定义迭代对象。生成器异常强大，网上你可以找到它联合`Promises`一起使用的情形，它为ajax异步调用开启一个新的世界，一个没有`callbacks`，没有`then`的世界，它的强大会超乎你的想象。

```js
// 基本用法
function* numberGen() {
  let limit = 3, i = 0;

  do {
    yield i++;
  } while (i < limit);
}

let iter = numberGen();

// -> { value: 0, done: false }
iter.next();

// -> { value: 1, done: false }
iter.next();

// -> { value: 2, done: false }
iter.next();

// -> { value: undefined, done: true }
iter.next();

// 过滤偶数
let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

function* even(numbers) {
  for (let n of numbers) {
    if (n % 2 === 0) {
      yield n;
    }
  }
}

for (let n of even(numbers)) {
  console.log(n);
}

// 延伸用法1
let janeDoe = {
  first: 'jane',
  last: 'doe'
};

function* iterObj(obj) {
  for (let prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      yield [prop, obj[prop]];
    }
  }
}

// -> "first: jane"
// -> "last: doe"
for (let [key, value] of iterObj(janeDoe)) {
  console.log([key, value].join(': '));
}

// 延伸用法2
function Person(firstName, lastName) {
  this.firstName = firstName;
  this.lastName = lastName;
}

Person.prototype.greeting = function (name) {
  return 'Hello, ' + name;
};

// Person.prototype[Symbol.iterator]
Person.prototype['@@iterator'] = function* () {
  for (let prop in this) {
    if (this.hasOwnProperty(prop)) {
      yield [prop, this[prop]];
    }
  }
};

let johndoe = new Person('john', 'doe');

// -> "first: john"
// -> "last: doe"
for (let [key, value] of johndoe) {
  console.log([key, value].join(': '));
}
```

###9. Comprehensions

Python最早引入了`List Comprehensions(列表推导)`的概念，这一特性深受程序员的喜爱，这一特性继而引申出`Dict Comprehensions`及`Generator Comprehensions`。CoffeeScript设计时也参考了Python，它也有`Comprehensions`的概念。而作为日渐流行的JavaScript，这么好的东西怎么能错过呢？自然而然地它也成为了JavaScript的标配。
我们在操作数组的时候经常会使用`Array.prototype.map`和`Array.prototype.filter`方法，ES6为我们提供的`Comprehensions`简直可以称为这两个方法提供`语法糖(syntax sugar)`，其语法表达直白、简明、形象。

```js
let fruits = ['apple', 'orange', 'banana'];

// 传统应用
let ripeFruits = fruits.map(function (item) {
  return 'ripe ' + item;
});

let fruitsWithN = fruits.filter(function (item) {
  return item.indexOf('n') > -1;
});

console.log(ripeFruits);
console.log(fruitsWithN);

// 新式玩法
// 1. 数组推导(Array Comprehension)
let ripeFruits2 = ['ripe ' + item for (item of fruits)];
let fruitsWithN2 = [item for (item of fruits) if (item.indexOf('n') > -1)];
let ripeFruitsWithN = ['ripe ' + item for (item of fruits) if (item.indexOf('n') > -1)];

console.log(ripeFruits2);
console.log(fruitsWithN2);
console.log(ripeFruitsWithN);

// 2. 生成器推导(Generator Comprehension)
let iter = ('ripe ' + item for (item of fruits) if (item.indexOf('n') > -1));
console.log(iter.next()); // -> "ripe orange"
console.log(iter.next()); // -> "ripe banana"
```

###10. 箭头函数(Arrow Functions)

有关ES6箭头函数的介绍移步[这里](http://www.nczonline.net/blog/2013/09/10/understanding-ecmascript-6-arrow-functions/)参阅。


II、新的代码组织方式
----------------------------------------------------

### 1. 类(Classes)

移步[这里](https://github.com/google/traceur-compiler/wiki/LanguageFeatures#wiki-classes)以及[这里](http://www.nczonline.net/blog/2012/10/16/does-javascript-need-classes/)进行参阅。

### 2. 模块(Modules)

移步[这里](https://github.com/google/traceur-compiler/wiki/LanguageFeatures#wiki-modules)进行参阅。


III、新的标准类库
----------------------------------------------------

### 1. 集合(Set)

Python的作者是个数学家，所以这门语言早期就有了对`Set`的支持。现在，ES6也将`Set`纳为标配了。有了集合，数组去除已然不费吹灰之力了。
更详细的介绍请移步[这里](http://www.nczonline.net/blog/2012/09/25/ecmascript-6-collections-part-1-sets/)。

```js
// 创建集合实例
let items = new Set([1, 2, 2, 3, 4, 3, 5, '2']);

// 判断指定元素是否在集合中
console.log(items.has('2'));

// 遍历集合元素
for (let item of items) {
  console.log(item);
}

// 添加元素到集合中
items.add(6);

// 从集合中移除元素
items.delete(1);

// 获取集合里元素个数
console.log(items.size);

// 遍历集合元素
for (let item of items) {
  console.log(item);
}

// 移除集合里所有元素
items.clear();
```

###2. 映射(Map)

以往我们都是使用字面对象构建键值对映射，ES6提供的`Map`结构提供了友好直白的API让我们可以更好地操纵键值对，就像`localStorge`一样，它使我们更好地在客户端保存数据。
更详细的介绍请移步[这里](http://www.nczonline.net/blog/2012/10/09/ecmascript-6-collections-part-2-maps/)。

```js
// 创建映射实例
let stuff = new Map();

// 设置键值对
stuff.set('foo', 'bar')
// 你没看错，对象也可以作为Map的key
stuff.set(document, document.createElement('div'));

// 判断是否设置了指定键
console.log(stuff.has('foo'));

// 获取键值对个数
console.log(stuff.size);

// 获取指定键的值
console.log(stuff.get('foo'));

// 删除指定的键
stuff.delete('foo');

// 清除所有键
stuff.clear();

// 遍历键值对
for (let item of stuff) {
  // key = item[0];
  // value = item[1];
  // do something
}

// 同上
for (let item of stuff.items()) {
  // do something
}

// 同上(解构赋值)
for (let [key, value] of stuff) {
  // do something
}

// 遍历所有键
for (let key of stuff.keys()) {
  // do something
}

// 遍历所有值
for (let value of stuff.values()) {
  // do something
}
```

###2. 弱映射(WeakMap)

`WeakMap`和`Map`类似，但`WeakMap`的键只能为对象，而不能为原始类型。
有关`WeakMap`的详细的介绍请移步[这里](http://www.nczonline.net/blog/2012/11/06/ecmascript-6-collections-part-3-weakmaps/)以及[这里](http://www.nczonline.net/blog/2014/01/21/private-instance-members-with-weakmaps-in-javascript/)。

###3. Promises

由于JavaScript的异步编程的普遍应用，Promises尤显得重要。众望所归，ES6也把`Promises`写入草案中了。目前`Firefox 30+及Chrome33+`实现了`Promises`，加了这个[polyfill](https://github.com/jakearchibald/es6-promise)，我们可以在所有现代浏览器中使用它。

```js
function get(url) {
  return new Promise(function (resolve, reject) {
    var xhr = new XMLHttpRequest();

    xhr.open('GET', url);

    xhr.onload = function () {
      var status = xhr.status;

      if ((status >= 200 && status < 300) || status === 304) {
        resolve(xhr.response);
      } else {
        reject(xhr.statusText);
      }
    };

    xhr.onerror = function () {
      reject('Network error');
    };

    xhr.send(null);
  });
}

function getJSON(url) {
  return get(url).then(JSON.parse);
}

// file1.txt: { "message": "This is the first file." }
// file2.txt: { "message": "This is the second file." }
// file3.txt: 404

let promise = getJSON('file1.txt');

promise
  .then(function (obj) {
    alert(obj.message);
    return getJSON('file2.txt');
  })
  .then(function () {
    alert(obj.message);
    return getJSON('file3.txt');
  })
  .then(function (obj) {
    alert(obj.message);
  })
  .catch(console.log);
```

###3. 虚拟对象(Proxies)

`Proxies`实为虚拟对象，它为对象操纵添加了一道包装，使用它有点Ruby元编程的味道。更多关于`Proxies`的解释请参阅[这里](http://wiki.ecmascript.org/doku.php?id=harmony:direct_proxies)

```js
// 原型
let handler = {
  get: function (proxy, name) {
    console.log('Getter for ' + name);
  },

  set: function (proxy, name, value) {
    console.log('Setter for ' + name + ' and value of ' + value);
  },

  has: function (name) {
    console.log(name + ' is in the has trap.');
  }
};

var proxy = Proxy.create(handler);

// 实例
let createElement = (function () {
  let specialProps = ['id', 'className'];

  return function (tagName) {
    let element = document.createElement(tagName);

    let p = Proxy.create({
      get: function (proxy, name) {
        if (name === 'node') {
          return element;
        }

        if (name in element) {
          return element[name];
        }

        return element.getAttribute(name);
      },

      set: function (proxy, name, value) {
        if (name === 'node') {
          throw new Error('node cannot be set');
        }

        if (name in element) {
          if (specialProps.indexOf(name) === -1) {
            throw new Error(name + ' cannot be set');
          }

          element[name] = value;
        } else {
          element.setAttribute(name, value);
        }
      }
    });

    return p;
  };
})();

let el = createElement('div'); // proxy

el.id = 'proxyTest';
el.className = 'first-class';
el.classList.add('second-class');
el.foo = 'bar';
el['data-proxy-test'] = true;

console.log(el.node);
console.log(el.id);
console.log(el.className);
console.log(el.foo);
console.log(el['data-proxy-test']);
```

IV、尾声
----------------------------------------------------

更多关于ES6的信息可参阅如下链接：

1. [Addy Osmani ES6 Tools](https://github.com/addyosmani/es6-tools)
2. [Tracking ECMAScript 6 Support](http://addyosmani.com/blog/tracking-es6-support/)
3. [ES6 Support in Mozilla](https://developer.mozilla.org/en-US/docs/Web/JavaScript/ECMAScript_6_support_in_Mozilla)
4. [Kangax’s ES6 Support Table](http://kangax.github.io/es5-compat-table/es6/)
5. [ES6 Specification Wiki](http://wiki.ecmascript.org/doku.php?id=harmony:specification_drafts)
