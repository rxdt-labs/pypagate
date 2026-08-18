"""
A one-to-one reactified version of Python's built-in ``math`` module.
"""

import math as _math
from pypagate import register_func

# Number theoretic functions
comb = register_func(_math.comb)
factorial = register_func(_math.factorial)
gcd = register_func(_math.gcd)
isqrt = register_func(_math.isqrt)
lcm = register_func(_math.lcm)
perm = register_func(_math.perm)

# Floating point arithmetic
ceil = register_func(_math.ceil)
fabs = register_func(_math.fabs)
floor = register_func(_math.floor)
fmod = register_func(_math.fmod)
modf = register_func(_math.modf)
remainder = register_func(_math.remainder)
trunc = register_func(_math.trunc)

# Floating point mainuplation functions
copysign = register_func(_math.copysign)
frexp = register_func(_math.frexp)
isclose = register_func(_math.isclose)
isfinite = register_func(_math.isfinite)
isnan = register_func(_math.isnan)
ldexp = register_func(_math.ldexp)
nextafter = register_func(_math.nextafter)
ulp = register_func(_math.ulp)

# Power, exponential and logarithmic functions
cbrt = register_func(_math.cbrt)
exp = register_func(_math.exp)
exp2 = register_func(_math.exp2)
expm1 = register_func(_math.expm1)
log = register_func(_math.log)
log1p = register_func(_math.log1p)
log2 = register_func(_math.log2)
log10 = register_func(_math.log10)
pow = register_func(_math.pow)
sqrt = register_func(_math.sqrt)

# Summation and product functions
dist = register_func(_math.dist)
fsum = register_func(_math.fsum)
hypot = register_func(_math.hypot)
prod = register_func(_math.prod)

# Angular conversion
degrees = register_func(_math.degrees)
radians = register_func(_math.radians)

# Trigonometric functions
acos = register_func(_math.acos)
asin = register_func(_math.asin)
atan = register_func(_math.atan)
atan2 = register_func(_math.atan2)
cos = register_func(_math.cos)
sin = register_func(_math.sin)
tan = register_func(_math.tan)

# Hyperbolic functions
acosh = register_func(_math.acosh)
asinh = register_func(_math.asinh)
atanh = register_func(_math.atanh)
cosh = register_func(_math.cosh)
sinh = register_func(_math.sinh)
tanh = register_func(_math.tanh)

# Special functions
erf = register_func(_math.erf)
erfc = register_func(_math.erfc)
gamma = register_func(_math.gamma)
lgamma = register_func(_math.lgamma)

# Constants (NOTE: More for convenience)
pi = _math.pi
e = _math.e
tau = _math.tau
inf = _math.inf
nan = _math.nan
