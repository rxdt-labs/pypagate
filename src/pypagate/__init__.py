"""
Contains the fundamental building blocks of formulae: Terms, Formulas, and
Constants. It also provides basic arithmetic and conversion building blocks
for forming formulae.
"""

from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from numbers import Number
import operator
from typing import Any, Literal, Sequence


def evaluate(form: Formula | Term | Const) -> Any:
    """Given a Term or Formula get the *current* value it contains. For terms
    this is the same as .value method, but for for Formula, the entire
    expression is recursively evaluated.

    :param form: A formula (or term) to extract the current value of.
    :type form: class: Formula | Term
    :return: The *current* value of the Formula or Term.
    """
    # Basic building blocks are variables and constants (i.e. Terms)
    if isinstance(form, Term) or isinstance(form, Const) or (not form._needs_update):
        return form.value
    else: # Otherwise, recursively evaluate.
        vals = [evaluate(val) for val in form.operands]
        return form.op(*vals)

# String representation for unary and binary operations. Used in __str__ for
# a Formula

bin_str_map = {
    # Arithmetic operators.
    operator.add : '+',
    operator.mul : '*',
    operator.sub : '-',
    operator.truediv : '/',
    operator.floordiv : '//',
    operator.xor : '^',
    # Comparison operators.
    operator.lt : '<',
    operator.le : '<=',
    operator.eq : '==',
    operator.ne : '!=',
    operator.ge : '>=',
    operator.gt : '>'
}


unary_str_map = {
    operator.abs : 'abs',
    operator.not_ : 'not',
    operator.pos : '+',
    operator.neg : '-',
}


# Similar to here https://stackoverflow.com/a/7844038/667648
def register_bin_op(op: Callable[[Any, Any], Any]):
    """Helper function intended to help construct binary operations."""
    def b(self: Formula | Term, other: Formula | Term | Number | Literal | Const):
        if isinstance(other, Number):
            other = Const(other)
        assert isinstance(other, Formula) or isinstance(other, Term) or isinstance(other, Const)
        try:
            name = bin_str_map[op]
            formula = Formula(op=op, operands=[self, other], pos="infix", name=name)
            self._parents.append(formula)
            if not isinstance(other, Const):
                other._parents.append(formula)
            return formula
        except KeyError:
            formula = Formula(op=op, operands=[self, other], name=op.__name__)
            self._parents.append(formula)
            if not isinstance(other, Const):
                other._parents.append(formula)
            return formula
    return b

def register_rbin_op(op: Callable[[Any, Any], Any]):
    """Helper function intended to help construct binary operations (reversed)."""
    def b(self: Formula | Term, other: Formula | Term | Const | Number | Literal):
        if isinstance(other, Number):
            other = Const(other)
        assert isinstance(other, Term) or isinstance(other, Formula) or isinstance(other, Const)
        try:
            name = bin_str_map[op]
            formula = Formula(op=op, operands=[self, other], pos="infix", name=name)
            self._parents.append(formula)
            if not isinstance(other, Const):
                other._parents.append(formula)
            return formula
        except KeyError:
            formula = Formula(op=op, operands=[other, self], pos="infix", name=op.__name__)
            self._parents.append(formula)
            if not isinstance(other, Const):
                other._parents.append(formula)
            return formula
    return b

def register_unary_op(op: Callable[[Any], Any]):
    """Helper function intended to help construct unary operations."""
    def u(self: Formula | Term):
        try:
            name = unary_str_map[op]
            formula = Formula(op=op, operands=[self], pos="prefix", name=name)
            self._parents.append(formula)
            return formula
        except KeyError:
            formula = Formula(op=op, operands=[self], pos="prefix", name=op.__name__)
            self._parents.append(formula)
            return formula
    return u

def register_func(f: Callable):
    """Helper function intended to help construct unary operations."""
    def u(*args: Formula | Term):
        formula = Formula(op=f, operands=args, pos="prefix")
        for arg in args:
            if not isinstance(arg, Const):
                arg._parents.append(formula)
        return formula
    return u

def as_str(f: Term | Formula, excepts: dict | None=None):
    """
    Stringify the contents of a Formula. If you want to actually extract
    the values of a Formula, call ``str`` on it.

    :params f: The formula to convert.
    :params excepts: For special cases that `str` would not normally convert
    but you want to convert.
    """
    def safer_str(obj):
        try:
            return excepts[obj] # pyrefly: ignore
        except (KeyError, TypeError):
            return str(obj)
    formula = Formula(op=safer_str, operands=[f])
    f._parents.append(formula)
    return formula

def as_float(f: Term | Formula, excepts: dict | None=None):
    """
    Floatify the contents of a Formula. If you want to actually extract
    the values of a Formula, call float on it.

    :params f: The formula to convert.
    :params excepts: For special cases that `float` would not normally convert
    but you want to convert.
    """
    def safer_float(obj):
        try:
            return excepts[obj] # pyrefly: ignore
        except (KeyError, TypeError):
            return float(obj)
    formula = Formula(op=safer_float, operands=[f])
    f._parents.append(formula)
    return formula

def as_int(f: Term | Formula, excepts: dict | None=None):
    """
    Intify the contents of a Formula. If you want to actually extract
    the values of a Formula, call ``int`` on it.

    :params f: The formula to convert.
    :params excepts: For special cases that `int` would not normally convert
    but you want to convert.
    """
    def safer_int(obj):
        try:
            return excepts[obj] # pyrefly: ignore
        except (KeyError, TypeError):
            return int(obj)
    formula = Formula(op=safer_int, operands=[f])
    f._parents.append(formula)
    return formula


def as_bool(f: Term | Formula, excepts: dict | None=None):
    """
    Boolify the contents of a Formula. If you want to actually extract
    the values of a Formula, call int on it.

    :params f: The formula to convert.
    :params excepts: For special cases that `int` would not normally convert
    but you want to convert.
    """
    def safer_bool(obj):
        try:
            return excepts[obj] # pyrefly: ignore
        except (KeyError, TypeError):
            return bool(obj)
    formula = Formula(op=safer_bool, operands=[f])
    f._parents.append(formula)
    return formula

@dataclass
class Formula:
    """A Well-Formed-Formula that consists of Term objects (i.e. variables) and 
    operators."""
    op: Callable
    pos: str = "infix"
    name: str = "f"
    _value: Any = None
    operands: Sequence[Formula | Term | Const] = field(default_factory=list)    
    _parents: list[Formula] = field(default_factory=list)
    _binds: Any = field(default_factory=list)
    _fire_on: list[Callable] = field(default_factory=list)
    _on_change: list[Callable] = field(default_factory=list)
    _needs_update: bool = True

    def _update(self):
        # Capture the old truth state before mutation
        new_value = evaluate(self)
        
        if new_value != self._value:
            for func in self._on_change:
                func(self._value, new_value)
        
        self._value = new_value
        self._needs_update = False

        for parent in self._parents:
            parent._needs_update = True
            parent._update()
            
        for obj, field_name in self._binds:
            setattr(obj, field_name, self._value)
            
        for func in self._fire_on:
            if self.value:
                 func()

    def _propegate(self):
        for parent in self._parents:
            parent._needs_update = True
            parent._update()
        # Even a lonesome Term may be bound to a field.
        for obj, field_name in self._binds:
            setattr(obj, field_name, self._value)
        # or it may also be given a contract.
        if self.value:
            for func in self._fire_on:
                func()

    @property
    def value(self):
        """Get the value the formula currently evaluates to."""
        if self._needs_update:
            return evaluate(self)
        return self._value

    def __repr__(self):
        # Bypass Python's name mangling by directly accessing the runtime globals
        if self.pos == "prefix":
            # Unary operations only have one operand
            return self.name + " (" + repr(self.operands[0]) + ")"
        else:
            parens1 = ('', '')
            parens2 = ('', '')
            if isinstance(self.operands[0], Formula):
                parens1 = (' (', ') ')
            if isinstance(self.operands[1], Formula):
                parens2 = (' (', ') ')
            return parens1[0] + repr(self.operands[0]) + parens1[1] + " " + \
       self.name + parens2[0] + " " + repr(self.operands[1]) + parens2[1]

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def __bool__(self):
        return bool(self.value)
    
    # Binary operations
    __add__ = register_bin_op(operator.add)
    __radd__ = register_rbin_op(operator.add)
    __sub__ = register_bin_op(operator.sub)
    __rsub__ = register_rbin_op(operator.sub)
    __pow__ = register_bin_op(operator.pow)
    __rpow__ = register_rbin_op(operator.pow)
    __mul__ = register_bin_op(operator.mul)
    __rmul__ = register_rbin_op(operator.mul)
    __truediv__ = register_bin_op(operator.truediv)
    __rtruediv__ = register_rbin_op(operator.truediv)
    __floordiv__ = register_bin_op(operator.floordiv)
    __rfloordiv__ = register_rbin_op(operator.floordiv)
    __xor__ = register_bin_op(operator.xor)
    __rxor__ = register_rbin_op(operator.xor)

    # Unary operations
    __abs__ = register_unary_op(operator.abs)
    __not__ = register_unary_op(operator.not_)
    __pos__ = register_unary_op(operator.pos)
    __neg__ = register_unary_op(operator.neg)

    # Comparison operators. 
    # NOTE: We ignore bad-override error from Pyrefly. This is because normally
    # these operators return booleans, but we do *not* want to do that.
    __lt__ = register_bin_op(operator.lt) # pyrefly: ignore[bad-override]
    __rlt__ = register_rbin_op(operator.lt) # pyrefly: ignore[bad-override]
    __gt__ = register_bin_op(operator.gt) # pyrefly: ignore[bad-override]
    __rgt__ = register_rbin_op(operator.gt) # pyrefly: ignore[bad-override]
    __ge__ = register_bin_op(operator.ge) # pyrefly: ignore[bad-override]
    __rge__ = register_rbin_op(operator.ge) # pyrefly: ignore[bad-override]
    __eq__ = register_bin_op(operator.eq) # pyrefly: ignore[bad-override]
    __req__ = register_rbin_op(operator.eq) # pyrefly: ignore[bad-override]
    __ne__ = register_bin_op(operator.ne) # pyrefly: ignore[bad-override]
    __rne__ = register_rbin_op(operator.ne) # pyrefly: ignore[bad-override]

def _register_ibin_op(bin_op: Callable[[Any, Any], Any]):
    """Helper function intended to help construct binary operations (like 
    __radd__) for Formula and Term."""
    def b(self: Formula | Term, other: Number | Literal):
        new_value = bin_op(self._value, other)
        if new_value != self._value:
            # Something did change.
            # Execute _on_change funcs.
            for func in self._on_change:
                func(self._value, new_value)
            # Since it changed, also check truthiness and execute
            # corresponding functions.
            if self.value:
                for func in self._fire_on:
                    func()
        self._value = new_value
        self._propegate()
        return self
    return b


@dataclass
class Term:
    """Essentially a variable that may be updated by the user. Can be included
    in more complicated formula and whenever it is changed, the parent formula
    are also updated to reflect this change."""
    _value: Any = None
    # Parent formulas containing the variable.
    _parents: list[Formula] = field(default_factory=list)
    # Raw Python fields that should change on update of this Term.
    _binds: list[tuple[Any, Any]] = field(default_factory=list)
    # List of functions that are executed if this Term is True.
    _fire_on: list[Callable] = field(default_factory=list)
    _on_change: list[Callable] = field(default_factory=list)
    _var_count: int = 0 # Terms do not contribute variable count, but variables
                        # do!

    def _propegate(self):
        for parent in self._parents:
            parent._needs_update = True
            parent._update()
        # Even a lonesome Term may be bound to a field.
        for obj, field_name in self._binds:
            setattr(obj, field_name, self._value)
        # or it may also be given a contract.
        if self.value:
            for func in self._fire_on:
                func()

    def change(self, new_value):
        """Change the wrapped value of the term. (Internally updates formulas
        that use this term.)
        
        :param new_value: The value to change self._value to.
        """
        # Nothing actually changed.
        if self._value == new_value:
            return
        # Something did change.
        # Execute _on_change funcs.
        for func in self._on_change:
            func(self._value, new_value)
        # Execute _on_fire funcs if the Term has truthiness of True
        if self.value:
            for func in self._fire_on:
                func()
        # Continue updating.
        self._value = new_value
        self._propegate()

    @property
    def value(self):
        """Returns the value of the Term at the current moment."""
        return self._value

    def __repr__(self):
        return f'Var[{self.value}]'

    def __str__(self):
        return str(self._value)

    def __float__(self):
        return float(self._value)

    def __int__(self):
        return int(self._value)

    # Binary operators
    __add__ = register_bin_op(operator.add)
    __radd__ = register_rbin_op(operator.add)
    __sub__ = register_bin_op(operator.sub)
    __rsub__ = register_rbin_op(operator.sub)
    __pow__ = register_bin_op(operator.pow)
    __rpow__ = register_rbin_op(operator.pow)
    __mul__ = register_bin_op(operator.mul)
    __rmul__ = register_rbin_op(operator.mul)
    __truediv__ = register_bin_op(operator.truediv)
    __rtruediv__ = register_rbin_op(operator.truediv)
    __floordiv__ = register_bin_op(operator.floordiv)
    __rfloordiv__ = register_rbin_op(operator.floordiv)
    __xor__ = register_bin_op(operator.xor)
    __rxor__ = register_rbin_op(operator.xor)

    # Unary operators
    __abs__ = register_unary_op(operator.abs)
    __not__ = register_unary_op(operator.not_)
    __pos__ = register_unary_op(operator.pos)
    __neg__ = register_unary_op(operator.neg)
    
    # Comparison operators.
    # NOTE: We override bad-override because these operators *traditionally*
    # return a boolean but we want them to *not* do that.
    __lt__ = register_bin_op(operator.lt) # pyrefly: ignore[bad-override]
    __rlt__ = register_rbin_op(operator.lt) # pyrefly: ignore[bad-override]
    __gt__ = register_bin_op(operator.gt) # pyrefly: ignore[bad-override]
    __rgt__ = register_rbin_op(operator.gt) # pyrefly: ignore[bad-override]
    __ge__ = register_bin_op(operator.ge) # pyrefly: ignore[bad-override]
    __rge__ = register_rbin_op(operator.ge) # pyrefly: ignore[bad-override]
    __eq__ = register_bin_op(operator.eq) # pyrefly: ignore[bad-override]
    __req__ = register_rbin_op(operator.eq) # pyrefly: ignore[bad-override]
    __ne__ = register_bin_op(operator.ne) # pyrefly: ignore[bad-override]
    __rne__ = register_rbin_op(operator.ne) #pyrefly: ignore[bad-override]

    # In place assignment. NOTE: Although something like a += 1 should be the 
    # same as a = a + 1, it is *not* in this library. a += 1 changes increments
    # the term. a = a + 1 makes a become the formula a + 1.
    
    __iadd__ = _register_ibin_op(operator.iadd)
    __iand__ = _register_ibin_op(operator.iand)
    __itruediv__ = _register_ibin_op(operator.itruediv)
    __ifloordiv__ = _register_ibin_op(operator.ifloordiv)
    __ilshift__ = _register_ibin_op(operator.ilshift)
    __irshift__ = _register_ibin_op(operator.irshift)
    __imod__ = _register_ibin_op(operator.imod)
    __imul__ = _register_ibin_op(operator.imul)
    __imatmul__ = _register_ibin_op(operator.imatmul)
    __ior__ = _register_ibin_op(operator.ior)
    __ipow__ = _register_ibin_op(operator.ipow)
    __isub__ = _register_ibin_op(operator.isub)
    __ixor__ = _register_ibin_op(operator.ixor)

@dataclass
class Const:
    """Represents a constant Term. For efficiency purposes. Should not change so it has no parents."""
    value: Any

def bind(obj: Any, field_name: Any, form: Formula | Term):
    """Given an object and a field name, you can "bind" it to a Formula (or 
    Term). That is, whenever the Formula (or Term) is updated, the field for
    the object is also updated.

    :param obj: The object to update.
    :param field_name: The field specific field of `obj` to change.
    :param form: A Formula or Term that `obj.field` is updated to be equivalent
        to.
    """
    form._binds.append((obj, field_name))

def fire_on(form: Formula | Term, *args, **kwargs):
    """Use as a decorator: If a Formula's truthiness is True, call the
    decorated function.

    :param form: Execute the proceeding function if `form` evaluates to True at
        some point in time.
    :param args: Additional positional arguments to pass to the decorated function.
    :param kwargs: Additional keyword arguments to pass to the decorated function.
    """
    def fire_decorator(func):
        def wrapped():
            return func(*args, **kwargs)
        form._fire_on.append(wrapped)
        return func
    return fire_decorator

def permit(form: Formula | Term, *args, **kwargs):
    """Use as a decorator: If a Formula's truthiness is True, allow the
    decorated function to be called, otherwise calling the decorated function
    does nothing.

    :param form: *Allow* execution of the proceeding function if `form`
        evaluates to true at the time of calling the proceeding function.
    :param args: Additional positional arguments to pass to the decorated function.
    :param kwargs: Additional keyword arguments to pass to the decorated function.
    """
    def permit_decorator(func):
        def f(*f_args, **f_kwargs):
            if form.value:
                return func(*args, *f_args, **{**kwargs, **f_kwargs})
            else:
                return (lambda: None)()
        return f
    return permit_decorator

def either(form: Formula | Term, f: Callable[[], None], g: Callable[[], None]):
    """Creates a new function with name ``name`` that, when called, executes
    ``f`` when ``form`` is ``True`` and ``g`` when ``form`` is ``False``.

    :param form: ``Formula`` to test.
    :param f: Function to evaluate when ``form`` is ``True``.
    :param g: Function to evaluate when ``form`` is ``False``
    """
    def func():
        if form.value:
            return f()
        return g()
    return func

def on_change(form: Formula | Term, *args, **kwargs):
    """Use as a decorator: If a Formula's truthiness is True, call the
    decorated function.

    :param form: Execute the proceeding function if `form` evaluates to True at
        some point in time.
    :param args: Additional positional arguments to pass to the decorated function.
    :param kwargs: Additional keyword arguments to pass to the decorated function.
    """
    def fire_decorator(func):
        def wrapped(old, new):
            return func(old, new, *args, **kwargs)
        form._on_change.append(wrapped)
        return func
    return fire_decorator
