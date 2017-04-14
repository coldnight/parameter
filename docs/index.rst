.. parameter documentation master file, created by
   sphinx-quickstart on Fri Apr 14 14:51:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to parameter's documentation!
=====================================

`Parameter <https://github.com/coldnight/parameter>`_ is using to get and check HTTP parameters like use ORM.


Benefits
---------

* Less code to check arguments.
* Pass http arguments to other function with a single object.
* IDE friendly, IDE can easily detect the complation.
* Easy to linter, the linter can easily detect attribute error.


Example with tornado
---------------------


Normal pattern
^^^^^^^^^^^^^^^

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

Parameter pattern
^^^^^^^^^^^^^^^^^^

.. code:: python

    from tornado import web

    from parameter import Model, Argument
    from parameter import types
    from parameter.adapter import TornadoAdapter


    class DemoEntity(Model):
        action = Argument("action", types.String, required=False,
                          miss_message="Please choose action", 
                          invalid_message="Invalid action")
        arg1 = Argument("arg1", types.Integer)
        arg2 = Argument("arg2", types.Double)
        # ...


    class DemoHandler(web.RequestHandler):
        def get(self):
            demo = DemoEntity(TornadoAdapter(self))
            do(demo)

Contents:


.. toctree::
   :maxdepth: 2

   guide.rst
   types.rst
   adapter.rst
   exception.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

