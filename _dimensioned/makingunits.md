---
title: Create a unit system
layout: project
project: dimensioned
date: 2015-6-6
version: 0.2.2
---

In addition to supplying multiple unit systems for your use, `dimensioned` provides a
convenient macro for creating your own. Let us look at a brief
[example](https://github.com/paholg/dimensioned/blob/master/examples/fruit.rs):

```rust
#[macro_use]
extern crate dimensioned;

make_units!{
    Fruit, Unitless, one;
    base {
        Apple, apple, a;
        Banana, banana, b;
        Cucumber, cuke, c;
        Mango, mango, m;
        Watermelon, watermelon, w;
    }
    derived {
    }
}

fn main() {
    let fruit_salad = apple * banana * mango * mango * watermelon;
    // prints "Mmmm, delicious: 1 a*b*m^2*w":
    println!("Mmmm, delicious: {}", fruit_salad);
}
```
There's a little bit going on here, so let's take a look. The first line,

```rust
Fruit, Unitless, one;
```

names the unit system `Fruit` and creates the type `Unitless` representing a dimensioned
type with no dimensions, and the corresponding constant `one`, which looks like this:

```rust
pub const one: Dim<Unitless, f64> = Dim::new(1.0);
```

The, the `base` block is used to define the base units of the system. The line

```rust
Apple, apple, a;
```

defines the type `Apple`, the corresponding constant `apple` (which also has a value of
`1.0f64`), and will use the token "a" for printing things of `Apple` type. The type
signature of `apple` is

```rust
Dim<Apple, f64>
```

and it is this type signature that will be
useful for writing functions that take specific dimensioned quantities. You will
probably never want to use `Apple` by itself.

Note that `Apple` is just a convenient name for the full type signature, which is given by

```rust
type Apple = Fruit<One, Zero, Zero, Zero, Zero>;
```

While you should never need to use this signature directly, it will crop up in error
messages, so it's good to be aware of it.

The derived block is currently a placeholder, but will used for naming types and
creating constants for derived units.


If you want a bit more flexibility when creating a unit system, there is a second macro
with a few more options. Here is its use in defining the
[CGS](https://github.com/paholg/dimensioned/blob/master/src/cgs.rs) system:

```rust
make_units_adv! {
    CGS, Unitless, one, f64;
    base {
        Two, Centimeter, centimeter, cm;
        Two, Gram, gram, g;
        One, Second, second, s;
    }
    derived {
    }
}
```

The first line is as before, but with an extra item; the type that you wish to use for
your defined constants. Right now it is mostly a placeholder (only `f32` and `f64` will
work), but once associated constants arrive, it will be able to be anything that
implements `std::num::One`.

The lines defining base units also have an extra item, in front. It corresponds to the
highest root that you wish to allow for your units. In almost all cases, it will be
`One`, but in the CGS system, for example, the square root of centimeters and of grams
are well-defined, useful units, so a `Two` is used for each of them.

The numbers used are from the `peano` module, and you may use anything from `One` to
`Ten`. If for some reason you need something higher, you can define it as so:

```rust
use dimensioned::peano::{Ten, Succ};

type Eleven = Succ<Ten>;
```

It is quite possible that more features will be added to `make_units_adv!()`, but the
goal is to keep `make_units!()` as simple as possible.
