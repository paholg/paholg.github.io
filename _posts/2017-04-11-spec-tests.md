---
title: Specializing tests
layout: post
---

I recently published a new version of [dimensioned](https://crates.io/crates/dimensioned/), a Rust
library for compile-time dimensional analysis. In so doing, I found a neat little pattern coupling
[specialization](https://github.com/rust-lang/rfcs/pull/1210/) with test generation.

## The Problem

Among other things, dimensioned defines various unit systems, and many constants in each unit
system. All of this is performed by a build script that creates documentation at the same time. For
example, from [this code](https://github.com/paholg/dimensioned/blob/master/src/build/si.rs),
[this documentation](http://paholg.com/dimensioned/dimensioned/unit_systems/si/index.html) is
created.

In addition to generating documentation, we would like to generate some tests. One such test is to
compare constants across unit systems. If the same constant is defined in two unit systems, then we
should ensure that, when converted, they have the same value. This ensures both that the conversion
does what it should and that we haven't made a typo when defining one of the constants.

Given unit systems `a` and `b`, it should be as easy as

```rust
assert_ulps_eq!(a::CONST, b::CONST.into(),
                epsilon = a::A::new(0.0),
                max_ulps = 2);
```

Note: Due to the non-associativity of floating point math, we can't use
`assert_eq!`. Instead, we verify that the constants are within 2
[ULPS](https://en.wikipedia.org/wiki/Unit_in_the_last_place) using the
[approx](https://github.com/brendanzab/approx) crate.

Unfortunately, this fails. We can't always convert from `a` to `b`. Or, sometimes we can convert
from `a` to `b`, but we can't go from `b` to `a`. For example, we can convert from SI to the
centimeter-gram-second (CGS) system, but only from a subset of SI. We can't convert a candela to
CGS; there's no unit to represent it. In addition, it makes no sense to convert from CGS to SI, as
CGS represents electricity and magnitism units in terms of centimeters, grams, and seconds, so such
a conversion would be ambiguous.

What this means is `From` isn't implemented for all possible constants from all possible constants,
so we'll get `unimplemented` errors for some of those `into()` calls.

We could set up either a whitelist or blacklist of what constants to compare, but
that would be a pain and a maintainibility nightmare. Fortunately, there's a better way.

## The Solution

First, let's make a trait for performing these comparisons:

```rust
pub trait CmpConsts<B> {
    fn test_eq(self, b: B);
}
```

Then, let's implement it for when we can perform the conversion:

```rust
impl<A, B> CmpConsts<B> for A where
    A: From<B> +
       fmt::Debug +
       Dimensioned<Value=f64> +
       ApproxEq<Epsilon=Self>
{
    fn test_eq(self, b: B) {
        assert_ulps_eq!(self, b.into(), epsilon = A::new(0.0), max_ulps = 2);
    }
}
```

So, when we call `a.test_eq(b)`, we perform the same test as before, with the same problems. So far
we have done nothing but added a useless layer of abstraction. Yay us!

However, with a default `impl`, it suddenly becomes useful:

```rust
impl<A, B> CmpConsts<B> for A {
    default fn test_eq(self, _: B) {
    }
}
```

Now, `CmpConsts` is implemented for *any* two types `A` and `B`. If we can convert from `B` to `A`,
then we perform the test. If not, then we do nothing and move on. No more compiler errors, and we
can generate all the comparison tests we want!
