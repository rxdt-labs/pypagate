=========
Internals
=========

We give a brief overview of how ``pypagate`` works internally. Operator overloading, some tree traversal, and three major classes (``Formula``, ``Term``, and ``Const``) make this library possible.

-----------
The Classes
-----------

There are three major classes:

- ``Term``: Kind of like a variabble you can choose the value of.
- ``Const``: A simplified ``Term`` for efficiency puproses.
- ``Formula``: A combination of functions, terms, and constants that describe a mathematical formula.

.. note:: What about ``Const``?
   We will not cover ``Const`` in this overview. Suffice to say, it is basically a ``Term`` that cannot change, thus, it just has fewer features than ``Term`` objects. It is included for efficiency puprposes.

----------------
``Term`` Objects
----------------

A ``Term`` has

- an internal value
- a list of parents
- a function to notify parents it changed.

Nearly everything else in the ``Term`` class is operator overloading to make it work like a normal variable. It is worth pointing out: For the overloaded operators, a ``Formula`` object is always returned. Furthermore, in an expression like ``x + y`` (where ``x`` and ``y`` are ``Term`` objects), ``x`` and ``y`` are given ``x + y`` as a parent. This way, if either ``x`` or ``y`` changes, they can notify ``x + y`` it should also change.

.. warning:: Boolean operators
   Boolean operators like ``==`` and ``!=`` *also* return a ``Formula``. So, *do not* use them in an ``if`` statement or ``while`` loop. They will not behave as expected. This is intentional, if a bool was returned there would be no way for auto updating.

-------------------
``Formula`` Objects
-------------------

``Formula`` are a bit trickier. They have a recursive definition. A formula has children ``Formula`` (or ``Term`` objects) and an operation. A condensed version of the ``Formula`` class looks like:

.. code-block:: python
   
   @dataclass
   class Formula:
       op: Callable
       operands: list[Any]

Let's look at an example:

.. code-block:: python

   w = (x + y) + z

This means that ``w`` is the formula ``x + y`` combined with the term ``z``. Thus, ``w`` has the binary operator ``+`` and children corresponding to ``x + y`` and ``z``.

Let's consider what happens if ``z`` is changed. ``z`` updates its value. Then ``z`` notifies the parent ``w`` it has been updated. ``w`` tries to notify their parents, but it has none and nothing else is notified. ``w`` then realizes it needs to update. So, it applies ``+`` the two children it has: ``x + y`` and ``z``. Since ``x + y`` did not change a cached value is used. ``z`` updated *before* ``w`` so a cached (but current) value of ``z`` is used. Ignoring caching, and assuming each formula has two children, updating a ``Formula``, say ``f``, is a recursive call: ``eval(f) = f.bin_op(eval(f.lhs), eval(f.rhs))``.

Since we allow for more than just binary operators, the expression more closely resembles:

.. code-block:: python

   eval(f) = f.op(map(eval, f.children))

That is, evaluate each child, then combine all the children with the operation.
