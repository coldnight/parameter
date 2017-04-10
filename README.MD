# Parameter

像使用 ORM 一样定义和检查 HTTP 参数.

想象一下一个 HTTP 请求有非常多的参数需要获取校验并传递到对应的函数里,
这将会产生非常多的获取参数代码和校验参数代码, 同时对应的函数需要定义为接收非常多的参数,
这样代码会非常臃肿且不清晰, 所以能不能像使用 ORM 那样预先在一个类中声明接收的参数,
并在后续的使用中使用该类的对象.


```python
from tornado import web


class DemoHandler(web.RequestHandler):
    def get(self):
        action = self.get_argument("action", None)
        arg1 = self.get_argument("arg1", None)
        arg2 = self.get_argument("arg2", None)

        # ...

        if action:
            pass

        if arg1:
            pass

        # ...

        do(action, arg1, arg2, ...)

```

使用 `parameter`

```python
from tornado import web

from parameter import Model, Argument
from parameter import ArgumentError, ArgumentMissError, ArgumentInvalidError
from parameter import types
from parameter.adapter import TornadoAdapter


class DemoParameter(Model):
    action = Argument("action", types.String, required=False,
                      miss_message="请选择动作", invalid_message="动作不合法")
    arg1 = Argument("arg1", types.Integer)
    arg2 = Argument("arg2", types.Double)
    # ...


class DemoHandler(web.RequestHandler):
    def get(self):
        try:
            demo = DemoParameter(TornadoAdapter(self))
        except ArgumentError as e:
            if isinstance(e, ArgumentMissError):
                self.set_status(405)
                self.write(e.message)
            elif isinstance(e, ArgumentInvalidError):
                self.write(e.message)
            return

        do(demo)
```


## 目标

- 易于使用
- 易于扩展
