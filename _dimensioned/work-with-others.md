---
title: Work with other types
layout: project
project: dimensioned
nav: [[Example A, ExampleA], [Example B, ExampleB], [Example C, ExampleC]]
date: 2015-6-9
version: 0.2.3
---

One goal of dimensioned is to be usable anywhere one might wish as effortlessly as
possible. To this end, I have created a few examples of using it with different
types. The first two examples cover using dimensioned with a type that knows nothing of
its existence, and in the third I create a type designed to use with dimensioned.

All three examples do the same thing; use a 3-vector to do some basic physical
computations.


### <a name="ExampleA"></a> Example A - Working with a type that expects primitives


If you'd rather look at code than read all this, you can.

* [Example A](https://github.com/paholg/dimensioned/blob/master/examples/vector3a.rs)
* [Example B](https://github.com/paholg/dimensioned/blob/master/examples/vector3b.rs)
* [Example C](https://github.com/paholg/dimensioned/blob/master/examples/vector3c.rs)

First, we define a basic `Vector3` that only uses `f64`. It is defined as
follows:

```rust
#[derive(Copy, Clone, PartialEq, PartialOrd)]
pub struct Vector3 {
    x: f64,
    y: f64,
    z: f64,
}

impl Vector3 {
    #[inline]
    pub fn new(x: f64, y: f64, z: f64) -> Vector3 {
        Vector3{ x: x, y: y, z: z}
    }

    #[inline]
    pub fn cross(self, rhs: Vector3) -> Vector3 {
        Vector3{ x: self.y*rhs.z - self.z*rhs.y,
                 y: self.z*rhs.x - self.x*rhs.z,
                 z: self.x*rhs.y - self.y*rhs.x }
    }
    #[inline]
    pub fn dot(self, rhs: Vector3) -> f64 {
        self.x*rhs.x + self.y*rhs.y + self.z*rhs.z
    }
    #[inline]
    pub fn norm2(self) -> f64 {
        self.dot(self)
    }
    #[inline]
    pub fn norm(self) -> f64 {
        self.norm2().sqrt()
    }
}
```

In addition, the operators for addition, subtraction, and scalar multiplication and
division are defined. You can view the full implementation as well as a full example
[here](https://github.com/paholg/dimensioned/blob/master/examples/vector3a.rs).


Now, let us use it with dimensioned. First, let's import the constants that we care
about.

```rust
use dimensioned::si::{one, m, kg, s}
```

We could also create our own unit system, but SI will serve our purposes fine.

In order to use the unit system with `Vector3`, we will work with objects of type `Dim<D, Vector3>`, which we can
most easily create with

```rust
let xhat = one * Vector3::new(1.0, 0.0, 0.0);
```

The variable `xhat` now has type `Dim<Unitless, Vector3>`. Note that this line requires
a couple things. First, `Vector3` must have implemented multiplication for scalars on the
left hand side, as follows:

```rust
impl Mul<Vector3> for f64 {
    ...
}
```

Second, the dimensioned quantity must appear on the left; `Vector3::new(1.0, 0.0, 0.0) *
one` will not compile and, unless we implement it in `Vector3`'s crate, we cannot
implement it. Someday Rust's coherence rules may allow implementing this in the
dimensioned crate in a generic way, but it would be difficult to do so in a sensible,
non-abusable way.

Alternatively, we could define `xhat` with

```rust
let xhat: Dim<Unitless, Vector3> = Dim::new(Vector3::new(1.0, 0.0, 0.0));
```

Now that we have `xhat`, we can multiply, divide, add, and subtract with no extra
work. Assuming we have similarly defined `yhat`, we can do all of

```rust
3.0*m*xhat + m*yhat;
13.0*m*xhat;
2.0*xhat/s;
```

and more. The only difficulty now is calling member functions of `Vector3`. We have a
few options. One way is to use the `wrap()` member of `Dim`:

```rust
let a = 3.0*m*xhat + 4.0*m*yhat;
let b = x.wrap((x.0).norm()); // type Dim<Meter, f64> with value 5.0
```

The expression `a.wrap(b)` gives `b` the dimensions of `a`. But, this is cumbersome and
messy.

There's a better way. There are a couple helper macros that can make
member functions of type `T` usable by `Dim<D, T>`. For norm, we could add this line:

```rust
dim_impl_unary!(Norm, norm, KeepDim, Vector3 => f64);
```

which expands to this:

```rust
pub trait Norm {
    type Output;
    fn norm(self) -> Self::Output;
}
impl<D> Norm for Dim<D, Vector3> where D: Dimension + KeepDim, <D as KeepDim>::Output: Dimension {
    type Output = Dim<<D as KeepDim>::Output, f64>;
    fn norm(self) -> Self::Output {
        Dim::new( (self.0).norm() )
    }
}
```

This creates a trait called `Norm` with a single function, `norm`. It expects `norm` to
be a member of `Vector3` and to return `f64`. `KeepDim` is a trait that functions as an
operator on dimensions. Available "operator traits" are


* `MulDim<RHS = Self>`
  * Mutiplies two dimensions together.
* `DivDim<RHS = Self>`
  * Divides one dimension by another.
* `PowerDim<RHS>`
  * Expects a peano number and raises a dimension to that power; for example `MulDim` is the same as `PowerDim<Two>`
* `RootDim<RHS>`
  * Expects a peano number and takes that root of the dimension; `RootDim<Two>` would be used for square root.
* `KeepDim<RHS = Self>`
  * Does not change the dimensions (but enforces that `RHS` is the same as `Self`).
* `InvertDim`
  * Inverts all the dimensions (e.g. seconds &#8594; hertz)

There is also a macro for member functions that take a single argument. We can implement
dot and cross products like so

```rust
dim_impl_binary!(Dot, dot, MulDim, Vector3 => f64);
dim_impl_binary!(Cross, cross, MulDim, Vector3 => Vector3);
```

Note that this macro expects the argument to be of the same type as the caller. If we
need more flexibility, then we can manually do what these macros do without too much
difficulty. For this example, at least, nothing else is necessary, and we can run the
full gamut of vector operations.

### <a name="ExampleB"></a>Example B - Working with a generic type


### <a name="ExampleC"></a>Example C - Creating a type to use with dimensioned

