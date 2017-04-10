.. image:: https://travis-ci.org/coldnight/parameter.svg?branch=master
    :target: https://travis-ci.org/coldnight/parameter
.. image:: https://codecov.io/github/coldnight/parameter/coverage.svg?branch=master
    :target: https://codecov.io/gh/coldnight/parameter
.. image:: https://img.shields.io/pypi/v/parameter.svg
    :target: https://pypi.python.org/pypi/parameter

Parameter
##########

Get and check HTTP parameters like use ORM.

Imaging you have a lot parameters to get and check, and also you need to pass those
parameters to a function. You will write a lot code to do this, this made code bloat
and ugly. So this libary let you get and check HTTP parameters like use ORM:

You define the parameters in a class, and then use the instance of the class to pass
to a function and something else.

Without parameter
------------------


.. code:: python

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

With `parameter`
-----------------

.. codeblock:: python

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


Installation
-------------

Use pip to install:

.. codeblock:: shell

    $ pip install parameter


Documentation
----------------

Coming soon.
