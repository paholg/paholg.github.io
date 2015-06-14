---
title: Work with other types
layout: project
project: dimensioned
nav: [[Example A, ExampleA], [Example B, ExampleB]]
---

One goal of dimensioned is to be usable anywhere as effortlessly as possible. To this
end, I have created a couple examples of using it with different types.

The first example covers using dimensioned with a non-generic type. This is the simplest
way to use it, but requires some setup.

The second example covers using dimensioned with a fully generic type. If the type is
generic enough, then this can be done with virtually no setup, but comes with some
caveats.

Both examples do the same thing; use a 3-vector to do some basic physical
computations.

There are similar examples included in dimensioned, and if you'd rather see them, you can:

* [Example A](https://github.com/paholg/dimensioned/blob/master/examples/vector3a.rs)
* [Example B](https://github.com/paholg/dimensioned/blob/master/examples/vector3b.rs)

### <a name="ExampleA"></a> Example A - Working with a type that expects primitives

#---vector-ex-a.md
title: Example A
layout: project
project: dimensioned
---#

First, we define a basic `Vector3` that only uses `f64` as follows:

```prelude
# #[macro_use]
# extern crate dimensioned;
# use std::ops::{Mul, Div, Add, Sub};
# use std::fmt::{self, Display};
# use dimensioned::{Dim};
# use dimensioned::si::{Unitless};

#[derive(Copy, Clone)]
pub struct Vector3 {
    x: f64,
    y: f64,
    z: f64,
}
impl Vector3 {
    fn new(x: f64, y: f64, z: f64) -> Vector3 {
        Vector3 {x: x, y: y, z: z}
    }
    fn cross(self, rhs: Vector3) -> Vector3 {
        Vector3::new(self.y*rhs.z - self.z*rhs.y,
                     self.z*rhs.x - self.x*rhs.z,
                     self.x*rhs.y - self.y*rhs.x)
    }
    fn dot(self, rhs: Vector3) -> f64 {
        self.x*rhs.x + self.y*rhs.y + self.z*rhs.z
    }
    fn norm2(self) -> f64 {
        self.dot(self)
    }
    fn norm(self) -> f64 {
        self.norm2().sqrt()
    }
}
```

We also want to implement the operators for addition, subtraction, and scalar
multiplication and division:

```prelude
impl Add<Vector3> for Vector3 {
    type Output = Vector3;
    fn add(self, rhs: Vector3) -> Self::Output {
        Vector3{ x: self.x + rhs.x, y: self.y + rhs.y, z: self.z + rhs.z }
    }
}
impl Sub<Vector3> for Vector3 {
    type Output = Vector3;
    fn sub(self, rhs: Vector3) -> Self::Output {
        Vector3{ x: self.x - rhs.x, y: self.y - rhs.y, z: self.z - rhs.z }
    }
}
impl Mul<f64> for Vector3 {
    type Output = Vector3;
    fn mul(self, rhs: f64) -> Self::Output {
        Vector3{ x: self.x * rhs, y: self.y * rhs, z: self.z * rhs }
    }
}
impl Div<f64> for Vector3 {
    type Output = Vector3;
    fn div(self, rhs: f64) -> Self::Output {
        Vector3{ x: self.x / rhs, y: self.y / rhs, z: self.z / rhs }
    }
}
impl Display for Vector3 {
    fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
        write!(f, "({}, {}, {})", self.x, self.y, self.z)
    }
}
```

Now, let us use it with dimensioned. First, let's import the constants that we care
about.

```prelude
use dimensioned::si::{one, m, kg, s};
```

We could also create our own unit system, but SI will serve our purposes fine.

In order to use the unit system with `Vector3`, we will work with objects of type
`Dim<D, Vector3>`, which we can most easily create with

```main
let xhat = one * Vector3::new(1.0, 0.0, 0.0);
```

The variable `xhat` now has type `Dim<Unitless, Vector3>`. Note that this line requires
a couple things. First, in addition the operators already defined, we must define
multiplication by `Vector3` for `f64`

```prelude
impl Mul<Vector3> for f64 {
    type Output = Vector3;
    fn mul(self, rhs: Vector3) -> Vector3 {
        Vector3::new(self*rhs.x, self*rhs.y, self*rhs.z)
    }
}
```

This allows us to perform scalar multiplication on vectors with the scalar on the
left.

Second, the dimensioned quantity must appear on the left; `Vector3::new(1.0, 0.0, 0.0) *
one` will not compile and we can't implement it as that would require being in the
dimensioned crate.

Alternatively, we could define a unit vector with

```main
let yhat: Dim<Unitless, Vector3> = Dim::new(Vector3::new(0.0, 1.0, 0.0));
```

Now that we have `xhat` and `yhat`, we can multiply, divide, add, and subtract with no extra
work.

```main
3.0*m*xhat + m*yhat;
13.0*m*xhat;
2.0*xhat/s;
```

and more. The only difficulty now is calling member functions of `Vector3`. We have a
few options. One way is to use `map`:

```main
let velocity = 3.0*m/s*xhat + 4.0*m/s*yhat;
let speed = velocity.map(Vector3::norm);
assert_eq!(speed, 5.0*m/s);
```

We do want to be careful with `map`, as while it can change the value type of a `Dim`
object, it cannot change its dimensions. We also may end up calling `norm()` many times
and it would be nice to do so with `velocity.norm()`.

Dimensioned provides a couple helper macros that can make member functions of type `T` usable by
`Dim<D, T>`. For `norm()`, we could add this line:

```ignore
dim_impl_unary!(Norm, norm, Same, Vector3 => f64);
```

which creates a trait `Norm` with a single function, `norm`. It expects `norm` to be a
member of `Vector3` that takes no other parameters that returns an `f64`.

`Same` is a trait that takes a type parameter and ensures that it is of type `Self`. The
trait that goes here functions as an operator on *types*, and it determines how the
member function we're implementing should affect our dimensions. The available options are

* `Same<RHS = Self>`: Does nothing to the dimensions but ensures that `RHS = Self`.
* `Mul<RHS = Self>`: Multiplies `Self` by `RHS`.
* `Div<RHS = Self>`: Divides `Self` by `RHS`.
* `Recip`: Gives the reciprocal of `Self`.
* `Pow<N>`: Raises `Self` to the exponent `N` where `N` is a Peano number.
* `Root<N>`: Takes the `N`th root of `Self` where `N` is a Peano number.
* `Sqrt`: Takes the square root of `Self`. The same as `Root<P2>`.
* `Cbrt`: Takes the cube root of `Self`. The same as `Root<P3>`.

To implement the square norm member, `norm2()`, we could use either `Mul` or `Pow<P2>`
for the operator trait:

```prelude
dim_impl_unary!(Norm2, norm2, Mul, Vector3 => f64);
```

The full expansion of the macro call for implementing `norm()` is

```prelude
# use dimensioned::{Dimension, Same};
pub trait Norm {
    type Output;
    fn norm(self) -> Self::Output;
}
impl<D> Norm for Dim<D, Vector3> where D: Dimension + Same, <D as Same>::Output: Dimension {
    type Output = Dim<<D as Same>::Output, f64>;
    fn norm(self) -> Self::Output {
        Dim::new( (self.0).norm() )
    }
}
```

There is also a macro for member functions that take a single argument. We can implement
the dot and cross products like so

```prelude
dim_impl_binary!(Dot, dot, Mul, Vector3 => f64);
dim_impl_binary!(Cross, cross, Mul, Vector3 => Vector3);
```

Here we can only use operator traits that take a type parameter "similar" to `Self`. They
are `Same`, `Mul`, and `Div`.

This macro expects the argument to have the same value type as the caller. If we need
more flexibility, then we can manually do what these macros do without too much
difficulty. For this example, at least, nothing else is necessary, and we can run the
full gamut of vector operations.


For fun, here are some:

```main
    let zhat = one * Vector3::new(0.0, 0.0, 1.0);
    let start = -22.0*xhat*m + 5.0*yhat*m + 6.0*zhat*m;
    println!("A physicist was standing on a hill at position {}.", start);

    let end = 26.0*xhat*m - 19.0*yhat*m;
    println!("Then she walked down the hill to {}.", end);

    let displace = end - start;
    println!("So, her displacement vector was {}.", displace);

    let time = 30.0*s;
    println!("The walk took her {}.", time);

    let velocity = displace/time;
    println!("She must have had an average velocity of {}.", velocity);

    let speed = velocity.norm();
    println!("So, her average speed was {}.", speed);
```

All of the code for this example is compiled into a single document (and tested every
library version) [here](examples/vector-ex-a.html), if you would like copy and run it,
or just view it all together.

### <a name="ExampleB"></a>Example B - Working with a generic type

#---vector-ex-b.md
title: Example B
layout: project
project: dimensioned
---#

Say you have a 3 dimensional vector library that is very generic; the coordinates can be
any type and (this is important) its operations are defined flexibly enough so that they
don't require types to be preserved. Fulfilling these requirements means that your
library will be a fair bit more verbose than the one above, but it can save some work
for using it with dimensioned.

We could still do everything as above and have objects with either type signature
`Dim<D, Vector3d<f64>>` or more generically `Dim<D, Vector3d<V>>`. This is what I would
still recommend.

We have another option, though, and that is what this example covers. We will end up
with objects with type signature `Vector3d<Dim<D, V>>`, essentially treating `Dim<D, V>`
as much like a primitive as possible.

```prelude
# extern crate dimensioned;
# extern crate num;
# use std::ops::{Add, Sub, Mul, Div};
# use num::traits::Float;
# use std::fmt::{self, Display};
# use dimensioned::si::{one, m, s, kg};

#[derive(Copy, Clone)]
pub struct Vector3<N> {
    x: N,
    y: N,
    z: N,
}

impl<N: Mul> Vector3<N> {
    pub fn new(x: N, y: N, z: N) -> Vector3<N> { Vector3{ x: x, y: y, z: z} }
}
```

In order to implement `Vector3<N>` generically enough to take `Dim` as its type
parameter, we need to put every member function in its own trait each with an associated
type.

Let's start with the dot product:

```prelude
pub trait Dot<N = Self> {
    type Output;
    fn dot(self, rhs: N) -> Self::Output;
}

impl<M, N> Dot<Vector3<N>> for Vector3<M> where M: Mul<N>, <M as Mul<N>>::Output: Add, <<M as Mul<N>>::Output as Add>::Output: Add<<M as Mul<N>>::Output> {
    type Output = <<<M as Mul<N>>::Output as Add>::Output as Add<<M as Mul<N>>::Output>>::Output;
    fn dot(self, rhs: Vector3<N>) -> Self::Output {
        self.x*rhs.x + self.y*rhs.y + self.z*rhs.z
    }
}
```

The `where` clause and the associated type `Output` are so messy because we can make no
assumptions about `N` or about what happens to its type signature when we add or
multiply it. We essentially have to represent the full expression `self.x*rhs.x +
self.y*rhs.y + self.z*rhs.z` as type operations, which have cumbersome syntax.

Fortunately, `dot` and `cross` are the worst offenders, and nothing else is as bad. Here
are the square norm and norm:

```prelude
pub trait Norm2 {
    type Output;
    fn norm2(self) -> Self::Output;
}
impl<N> Norm2 for Vector3<N> where Vector3<N>: Dot + Copy {
    type Output = <Vector3<N> as Dot>::Output;
    fn norm2(self) -> Self::Output { self.dot(self) }
}

pub trait Norm {
    type Output;
    fn norm(self) -> Self::Output;
}
impl<N> Norm for Vector3<N> where Vector3<N>: Norm2, <Vector3<N> as Norm2>::Output: Float {
    type Output = <Vector3<N> as Norm2>::Output;
    fn norm(self) -> Self::Output { self.norm2().sqrt() }
}
```

We do run into a problem, though, with `norm()`. It requires taking a square root, which
means we have to expect that `N` implements `Float`. However, `Dim` does not implement
`Float` as that would require implementing many functions that it doesn't make sense to
have for dimensioned quantities and other functions in a way that would not allow them
to change dimensions.

Fortunately, dimensioned provides a `Sqrt` trait that `Dim` does implement. A second
implementation of `Norm` conflicts with the first one and isn't possible if `Vector3<N>`
is defined in a different crate, but we can make a new trait;

```prelude
use dimensioned::{Dimension, Dim, Sqrt};

pub trait NormDim {
    type Output;
    fn norm(self) -> Self::Output;
}
impl<D: Dimension, V> NormDim for Vector3<Dim<D, V>> where Vector3<Dim<D, V>>: Norm2, <Vector3<Dim<D, V>> as Norm2>::Output: Sqrt {
    type Output = <<Vector3<Dim<D, V>> as Norm2>::Output as Sqrt>::Output;
    fn norm(self) -> Self::Output { self.norm2().sqrt() }
}

# pub trait Cross<N> {
#     type Output;
#     fn cross(self, rhs: N) -> Self::Output;
# }
# impl<M, N> Cross<Vector3<N>> for Vector3<M> where M: Mul<N> + Copy, N: Copy, <M as Mul<N>>::Output: Sub {
#     type Output = Vector3<<<M as Mul<N>>::Output as Sub<<M as Mul<N>>::Output>>::Output>;
#     fn cross(self, rhs: Vector3<N>) -> Self::Output {
#         Vector3{x: self.y*rhs.z - self.z*rhs.y,
#                 y: self.z*rhs.x - self.x*rhs.z,
#                 z: self.x*rhs.y - self.y*rhs.x}
#     }
# }
# impl<M, N> Add<Vector3<N>> for Vector3<M> where M: Add<N> {
#     type Output = Vector3<<M as Add<N>>::Output>;
#     fn add(self, rhs: Vector3<N>) -> Self::Output {
#         Vector3{x: self.x + rhs.x, y: self.y + rhs.y, z: self.z + rhs.z}
#     }
# }

# impl<M, N> Sub<Vector3<N>> for Vector3<M> where M: Sub<N> {
#     type Output = Vector3<<M as Sub<N>>::Output>;
#     fn sub(self, rhs: Vector3<N>) -> Self::Output {
#         Vector3{x: self.x - rhs.x, y: self.y - rhs.y, z: self.z - rhs.z}
#     }
# }

# // Scalar multiplication
# impl<N, T> Mul<T> for Vector3<N> where N: Mul<T>, T: Copy {
#     type Output = Vector3<<N as Mul<T>>::Output>;
#     fn mul(self, rhs: T) -> Self::Output {
#         Vector3{x: self.x * rhs, y: self.y * rhs, z: self.z * rhs}
#     }
# }

# // Scalar multiplication with the scalar on the left. There is not a generic way to do
# // this. Note that this requires multiplication by a scalar to be commutative!!!!!
# impl<N: Mul<f64>> Mul<Vector3<N>> for f64 {
#     type Output = Vector3<<N as Mul<f64>>::Output>;
#     fn mul(self, rhs: Vector3<N>) -> Self::Output {
#         rhs * self
#     }
# }

# // Scalar division
# impl<N, T> Div<T> for Vector3<N> where N: Div<T>, T: Copy {
#     type Output = Vector3<<N as Div<T>>::Output>;
#     fn div(self, rhs: T) -> Self::Output {
#         Vector3{x: self.x / rhs, y: self.y / rhs, z: self.z / rhs}
#     }
# }

# impl<N: Display> Display for Vector3<N> {
#     fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
#         write!(f, "({}, {}, {})", self.x, self.y, self.z)
#     }
# }
```

Similarly, we implement `Cross`, `Add`, `Sub`, `Div` for scalars, and `Mul` for scalars
both on the left and right. You can see the full implementations at the link at the
bottom of this example.

Now we can do the same operations as in Example A:

```main
let xhat = Vector3::new(one, 0.0*one, 0.0*one);
let yhat = Vector3::new(0.0*one, one, 0.0*one);
let zhat = Vector3::new(0.0*one, 0.0*one, one);

let start = -22.0*xhat*m + 5.0*yhat*m + 6.0*zhat*m;
println!("A physicist was standing on a hill at position {}.", start);

let end = 26.0*xhat*m - 19.0*yhat*m;
println!("Then she walked down the hill to {}.", end);

let displace = end - start;
println!("So, her displacement vector was {}.", displace);

let time = 30.0*s;
println!("The walk took her {}.", time);

let velocity = displace/time;
println!("She must have had an average velocity of {}.", velocity);

let speed = velocity.norm();
println!("So, her average speed was {}.", speed);
```

All of the code for this example is compiled into a single document (and tested every
library version) [here](examples/vector-ex-b.html), if you would like copy and run it,
or just view it all together.
