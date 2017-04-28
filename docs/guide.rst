Guide
=====

Installation
-------------

Use pip to install parameter.

.. code:: shell

    $ pip install -U parameter

Define model
-------------

Inherit from :class:`~parameter.model.Model` and use :class:`~parameter.model.Argument` to define
a model.

.. code:: python

    from parameter import Model, Argument
    from parameter import types

    class Person(Model):
        name = Argument(types.String)
        age = Argument(types.Integer)


After model defined, you can use an adapter to create a instance.

.. code:: python

    from parameter.adapter import JSONAdapter


    person = Person(JSONAdapter({"name": "Gray", "age": 18}))

    print(person.name)      # output: Gray
    print(person.age)       # output: 18


Alias
------

If a parameter's name is not same with the attribute name, we can use ``alias``.

.. code:: python

    from parameter import Model, Argument
    from parameter import types

    class Person(Model):
        children = Argument(types.String, alias="child", multiple=True)


The above code will map ``child`` argument to the ``children``.

List
----

If a parameter have mulitple arguments, just set ``mulitple=True`` in :class:`~parameter.model.Argument`.


.. code:: python

    from parameter import Model, Argument
    from parameter import types

    class Person(Model):
        name = Argument(types.String)
        age = Argument(types.Integer)
        children = Argument(types.String, alias="child", multiple=True)

    # Assume the request is: /person?name=Gray&age=18&child=Tom&child=Jim
    person = Person(DemoAdapter(request))

    print(person.name)      # output: Gray
    print(person.age)       # output: 18
    print(person.children)  # maybe output: ["Tom", "Jim"]


Nested
------

``parameter`` support nested by :class:`parameter.types.Nested`.

.. code:: python

    from parameter import Model, Argument
    from parameter import types
    from parameter.adapter import JSONAdapter

    class Person(Model):
        name = Argument(types.String)
        age = Argument(types.Integer)

    class Computer(Model):
        arch = Argument(types.String)
        belong = Argument(types.Nested(Person))


    computer = Computer(JSONAdapter({"arch": "x86", "belong": {"name": "Gray", "age": 10}}))

    assert computer.arch == "x86"
    assert isinstance(computer.person, Person)
    assert computer.person.name == "Gray"
    assert computer.person.age == 18


List nested
------------

``parameter`` nested also can be a list with ``mulitple`` argument.

.. code:: python

    from parameter import Model, Argument
    from parameter import types
    from parameter.adapter import JSONAdapter


    class Computer(Model):
        arch = Argument(types.String)


    class Person(Model):
        name = Argument(types.String)
        age = Argument(types.Integer)
        computers = Argument(types.Nested(Computer), multiple=True)


    person = Person(JSONAdapter({"name": "Gray", "age": 10, "computers": [
        {"arch": "x86"},
        {"arch": "x86_64"},
    ]}))

    assert person.name == "Gray"
    assert person.age == 18
    assert isinstance(person.computers, list)
    assert len(person.computers) == 2
    assert isinstance(person.computers[0], Computer)
    assert isinstance(person.computers[1], Computer)

    assert person.computers[0].arch == "x86"
    assert person.computers[1].arch == "x86_64"


Handling exception
-------------------

While creating model, there two exceptions that user must to care:

* :class:`parameter.exception.ArgumentMissError`: Raising when argument is missing
* :class:`parameter.exception.ArgumentInvalidError`: Raising when argument is invalid


Argument
---------

.. autoclass:: parameter.model.Argument
    :members:

    .. automethod:: parameter.model.Argument.__init__
