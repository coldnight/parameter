Guide
=====

Define model
-------------

Inherit from :class:`~parameter.model.Model` and use :class:`~parameter.model.Argument` to define
a model.

.. code:: python

    from parameter import Model, Argument
    from parameter import types

    class Person(Model):
        name = Argument("name", types.String)
        age = Argument("age", types.Integer)


After model defined, you can use an adapter to create a instance.

.. code:: python

    from parameter.adapter import JSONAdapter


    person = Person(JSONAdapter({"name": "Gray", "age": 18}))

    print(person.name)      # output: Gray
    print(person.age)       # output: 18


List
----

If an parameter have mulitple arguments, just set ``mulitple=True`` in :class:`~parameter.model.Argument`.


.. code:: python

    from parameter import Model, Argument
    from parameter import types

    class Person(Model):
        name = Argument("name", types.String)
        age = Argument("age", types.Integer)
        children = Argument("child", types.String, multiple=True)

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
        name = Argument("name", types.String)
        age = Argument("age", types.Integer)

    class Computer(Model):
        arch = Argument("arch", types.String)
        belong = Argument("belong", types.Nested(Person))


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
        arch = Argument("arch", types.String)


    class Person(Model):
        name = Argument("name", types.String)
        age = Argument("age", types.Integer)
        computers = Argument("computers", types.Nested(Computer), multiple=True)


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

While create model, there two exceptions user must to care:

* :class:`parameter.exception.ArgumentMissError`: Raising when argument is missing
* :class:`parameter.exception.ArgumentInvalidError`: Raising when argument is invalid


Argument
---------

.. autoclass:: parameter.model.Argument
    :members:

    .. automethod:: parameter.model.Argument.__init__
