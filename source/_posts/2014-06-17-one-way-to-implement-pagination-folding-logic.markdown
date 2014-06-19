---
layout: post
title: "简单的分页折叠逻辑实现"
date: 2014-06-19 10:28
comments: true
categories: [javascript]
---

列表数据量过多时，常见有以下两种呈现方式：

  * 将数据列表分页呈现
  * 采用瀑布流形式加载数据

本文单讲前者，即以分页方式呈现时分页折叠逻辑实现。

以往遇到需要分页的需求时，我一般采用项目中已经写好的公用组件直接用，或者利用第三方插件。观察这类代码的实现，有一个共同点：分页折叠逻辑和分页标签渲染是揉合在一块执行的。最近自己尝试着写了一个分页折叠逻辑实现，我把这部分逻辑从分页标签渲染中抽取出来了——我先处理分页折叠逻辑、再进而渲染分页标签。这么做有个好处：分页折叠逻辑和分页渲染处理实现解耦、职责区分，分页折叠逻辑代码的更换不会影响随后的渲染。

<!-- more -->

思考过程
-------------------

假设我们的数据有15页，如果不考虑分页折叠逻辑的话，我们分页显示大概像这样：

```js
//=> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
_.range(1, 15 + 1)
```
我们可以对以上这个数组遍历渲染为标签。然而我们的页面横向空间有限，分页过多时，我们不希望将每一页都显示为标签。我们需要将跟当前页不太相干的页号折叠起来，不管数据有多少页，只显示固定可视页就好。比如，当前页为第7页，且最多显示9个槽位，我们希望显示成这样：

```js
[1, '…', 5, 6, '7', 8, 9, '…', 15]
```

我们显示第一页、最末页以及与第7页相邻的页，其他页做折叠处理，即上述数组中的`…`，并且当前页显示为数字字符串以区分非当前页。

如果当前页是第2页呢？

```js
[1, '2', 3, 4, 5, 6, 7, '…', 15]
```

如果当前页是第12页呢？

```js
[1, '…', 9, 10, 11, '12', 13, 14, 15]
```

我们将分页折叠呈现用javascript的数组直接表示出来了，一切都很直观。既然这样，何不写个方法进行数组变换呢？我把这样的一个方法叫做`foldpages`：

```js
/**
 * [foldpages description]
 * @param  {[Array]}  pages    [未作变换的分页数组]
 * @param  {[Number]} current  [当前显示页]
 * @param  {[Number]} viewsize [分页显示槽位个数]
 * @return {[Array]}           [分页折叠后的数组]
 */
function foldpages(pages, current, viewsize) {}

var pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
var viewsize = 9;

//=> expected result: [1, '…', 5, 6, 7, 8, 9, '…', 15]
foldpages(pages, 7, viewsize);

//=> expected result: [1, 2, 3, 4, 5, 6, 7, '…', 15]
foldpages(pages, 2, viewsize);

//=> expected result: [1, '…', 9, 10, 11, 12, 13, 14, 15]
foldpages(pages, 12, viewsize);
```

剩下的就是实现了！

```js
var foldpages = function (pages, current, viewsize) {
  var ret  = [].concat(pages),
      min  = 1,
      max  = ret.length,
      dots = '…',
      remain;

  current = Math.max(min, Math.min(current, max));

  if (max <= viewsize) {
    ret[current - 1] = '' + ret[current - 1];
    return ret;
  }

  viewsize = Math.max(5, viewsize || 7);
  ret      = ['' + current];
  remain   = viewsize - 1;

  while (true) {
    var first = +ret[0], last = +ret[ret.length - 1];

    if (first > min)  {
      ret.unshift(first - 1);
      if (!--remain) break;
    }

    if (last < max) {
      ret.push(last + 1);
      if (!--remain) break;
    }
  }

  switch (true) {
  case +ret[0] === min:
    ret.splice(ret.length - 2, 2, dots, max);
    break;
  case +ret[ret.length - 1] === max:
    ret.splice(0, 2, min, dots);
    break;
  default:
    ret.splice(0, 2, min, dots);
    ret.splice(ret.length - 2, 2, dots, max);
    break;
  }

  return ret;
};
```

最后再验证下。

```js
var TOTAL_PAGE = 15;
var pages = _.range(1, TOTAL_PAGE + 1);

_.each(_.range(6, 10 + 1), function (foldnum) {
  console.log('当显示槽位个数为' + foldnum + '时，每一页的折叠显示如下:');

  _.times(TOTAL_PAGE, function (index) {
    console.log(++index, foldpages(pages, index, foldnum));
  });

  console.log('\n');
});

// =============================================
// OUTPUT
// =============================================

/**
当显示槽位个数为6时，每一页的折叠显示如下:
 1 ["1", 2, 3, 4, "…", 15]
 2 [1, "2", 3, 4, "…", 15]
 3 [1, 2, "3", 4, "…", 15]
 4 [1, 2, 3, "4", "…", 15]
 5 [1, "…", 4, "5", "…", 15]
 6 [1, "…", 5, "6", "…", 15]
 7 [1, "…", 6, "7", "…", 15]
 8 [1, "…", 7, "8", "…", 15]
 9 [1, "…", 8, "9", "…", 15]
10 [1, "…", 9, "10", "…", 15]
11 [1, "…", 10, "11", "…", 15]
12 [1, "…", 11, "12", "…", 15]
13 [1, "…", 12, "13", 14, 15]
14 [1, "…", 12, 13, "14", 15]
15 [1, "…", 12, 13, 14, "15"]

当显示槽位个数为7时，每一页的折叠显示如下:
 1 ["1", 2, 3, 4, 5, "…", 15]
 2 [1, "2", 3, 4, 5, "…", 15]
 3 [1, 2, "3", 4, 5, "…", 15]
 4 [1, 2, 3, "4", 5, "…", 15]
 5 [1, "…", 4, "5", 6, "…", 15]
 6 [1, "…", 5, "6", 7, "…", 15]
 7 [1, "…", 6, "7", 8, "…", 15]
 8 [1, "…", 7, "8", 9, "…", 15]
 9 [1, "…", 8, "9", 10, "…", 15]
10 [1, "…", 9, "10", 11, "…", 15]
11 [1, "…", 10, "11", 12, "…", 15]
12 [1, "…", 11, "12", 13, 14, 15]
13 [1, "…", 11, 12, "13", 14, 15]
14 [1, "…", 11, 12, 13, "14", 15]
15 [1, "…", 11, 12, 13, 14, "15"]

当显示槽位个数为8时，每一页的折叠显示如下:
 1 ["1", 2, 3, 4, 5, 6, "…", 15]
 2 [1, "2", 3, 4, 5, 6, "…", 15]
 3 [1, 2, "3", 4, 5, 6, "…", 15]
 4 [1, 2, 3, "4", 5, 6, "…", 15]
 5 [1, 2, 3, 4, "5", 6, "…", 15]
 6 [1, "…", 4, 5, "6", 7, "…", 15]
 7 [1, "…", 5, 6, "7", 8, "…", 15]
 8 [1, "…", 6, 7, "8", 9, "…", 15]
 9 [1, "…", 7, 8, "9", 10, "…", 15]
10 [1, "…", 8, 9, "10", 11, "…", 15]
11 [1, "…", 9, 10, "11", 12, "…", 15]
12 [1, "…", 10, 11, "12", 13, 14, 15]
13 [1, "…", 10, 11, 12, "13", 14, 15]
14 [1, "…", 10, 11, 12, 13, "14", 15]
15 [1, "…", 10, 11, 12, 13, 14, "15"]

当显示槽位个数为9时，每一页的折叠显示如下:
 1 ["1", 2, 3, 4, 5, 6, 7, "…", 15]
 2 [1, "2", 3, 4, 5, 6, 7, "…", 15]
 3 [1, 2, "3", 4, 5, 6, 7, "…", 15]
 4 [1, 2, 3, "4", 5, 6, 7, "…", 15]
 5 [1, 2, 3, 4, "5", 6, 7, "…", 15]
 6 [1, "…", 4, 5, "6", 7, 8, "…", 15]
 7 [1, "…", 5, 6, "7", 8, 9, "…", 15]
 8 [1, "…", 6, 7, "8", 9, 10, "…", 15]
 9 [1, "…", 7, 8, "9", 10, 11, "…", 15]
10 [1, "…", 8, 9, "10", 11, 12, "…", 15]
11 [1, "…", 9, 10, "11", 12, 13, 14, 15]
12 [1, "…", 9, 10, 11, "12", 13, 14, 15]
13 [1, "…", 9, 10, 11, 12, "13", 14, 15]
14 [1, "…", 9, 10, 11, 12, 13, "14", 15]
15 [1, "…", 9, 10, 11, 12, 13, 14, "15"]

当显示槽位个数为10时，每一页的折叠显示如下:
 1 ["1", 2, 3, 4, 5, 6, 7, 8, "…", 15]
 2 [1, "2", 3, 4, 5, 6, 7, 8, "…", 15]
 3 [1, 2, "3", 4, 5, 6, 7, 8, "…", 15]
 4 [1, 2, 3, "4", 5, 6, 7, 8, "…", 15]
 5 [1, 2, 3, 4, "5", 6, 7, 8, "…", 15]
 6 [1, 2, 3, 4, 5, "6", 7, 8, "…", 15]
 7 [1, "…", 4, 5, 6, "7", 8, 9, "…", 15]
 8 [1, "…", 5, 6, 7, "8", 9, 10, "…", 15]
 9 [1, "…", 6, 7, 8, "9", 10, 11, "…", 15]
10 [1, "…", 7, 8, 9, "10", 11, 12, "…", 15]
11 [1, "…", 8, 9, 10, "11", 12, 13, 14, 15]
12 [1, "…", 8, 9, 10, 11, "12", 13, 14, 15]
13 [1, "…", 8, 9, 10, 11, 12, "13", 14, 15]
14 [1, "…", 8, 9, 10, 11, 12, 13, "14", 15]
15 [1, "…", 8, 9, 10, 11, 12, 13, 14, "15"]
*/
```

分页折叠逻辑实现好了，接下的的分页渲染就信手拈来，不费吹灰之力了！

渲染分页
-------------------

直接上代码吧！

```js
var renderpages = function (pages) {
  return _.map(pages, function (page) {
    switch (true) {
    case page === +page: return '<a href="javascript:;">' + page + '</a>';
    case page ==  +page: return '<span class="current">' + page + '</span>';
    default:             return '<span>' + page + '</span>';
    }
  }).join('');
};

renderpages([1, '…', 5, 6, '7', 8, 9, '…', 15]);

//=>  '<a href="javascript:;">1</a>' +
      '<span>…</span>' +
      '<a href="javascript:;">5</a>' +
      '<a href="javascript:;">6</a>' +
      '<span class="current">7</span>' +
      '<a href="javascript:;">8</a>' +
      '<a href="javascript:;">9</a>' +
      '<span>…</span>' +
      '<a href="javascript:;">15</a>'
```

可以看到分页渲染时没有了分页折叠逻辑的干扰，代码清晰而简明了。我们一般都习惯把复杂的东西简单化。当然，要想要简单的事情变复杂化也是可行的。不信，我们以分页渲染为例，看能够将它复杂化到什么程度。

简单的事情复杂化
-------------------

仍是直接上代码的方式。

```js
function existy(x) { return x != null; }
function truthy(x) { return (x !== false) && existy(x); }

function cat() {
  var head = _.first(arguments);
  return existy(head) ?
         head.concat.apply(head, _.rest(arguments)) : [];
}

function construct(head, tail) {
  return cat([head], _.toArray(tail));
}

//=> [4, 8, 15, 16, 23, 42]
cat([4], [8, 15], [16, 23, 42]);

//=> [4, 8, 15, 16, 23, 42]
construct(4, [8, 15, 16, 23, 42]);

function dispatch(/* funs */) {
  var funs = _.toArray(arguments), size = funs.length;

  return function (target /*, args */) {
    var ret = undefined, args = _.rest(arguments);

    _.detect(funs, function (fun) {
      ret = fun.apply(fun, construct(target, args));
      return existy(ret);
    });

    return ret;
  };
}

function whilst(cond, action) {
  return function (obj) {
    return truthy(cond(obj)) ? action(obj) : undefined;
  };
}

var renderer = dispatch(
  whilst(
    function (x) { return x === +x; },
    function (x) { return '<a href="javascript:;">' + x + '</a>'; }
  ),
  whilst(
    function (x) { return x == +x; },
    function (x) { return '<span class="current">' + x + '</span>'; }
  ),
  function (x) { return '<span>' + x + '</span>'; }
);

var result = _.map([1, '…', 5, 6, '7', 8, 9, '…', 15], renderer).join('');
```

以上展示了如何用函数式编程方式把简单的事情复杂化。不过，它已背离了本文的宗旨，还是就此打住吧！

后记：想了好几种方式实现`foldpages`方法，天马行空的。然而，没有一种方式觉得很理想，包括贴在此处的这个！我想我是有代码洁癖症的，希望以后能想到更好的实现办法！这需要灵感：或是触类旁通的，或是恍然大悟的。

```js
var inspiration = _.result(aspiration, action);
```
