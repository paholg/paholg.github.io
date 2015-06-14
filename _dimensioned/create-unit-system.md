---
title: Create a unit system
layout: project
project: dimensioned
nav: [[Basic macro, basic], [Advanced macro, advanced]]
---


### <a name = "basic"></a>Basic macro

In addition to supplying multiple unit systems for your use, dimensioned provides a
convenient macro for creating your own. Let us look at a brief example. You can view all
of this code together [here](examples/create-units.html), where it has been tested and
confirmed to run with no errors.

```rust
#[macro_use]
extern crate dimensioned;

mod fruit {
    make_units! {
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
}
use fruit::{apple, banana, cuke, mango, watermelon};
```


There's a little bit going on here, so let's take a look. The first line inside the
macro,

```rust
Fruit, Unitless, one;
```

names the unit system `Fruit` and creates the type `Unitless` representing a dimensioned
type with no dimensions, and the corresponding constant `one`, defined as

```rust
pub const one: Dim<Unitless, f64> = Dim(1.0, PhantomData);
```

where `PhantomData` is just there because Rust doesn't allow function calls before main
(although this is changing for pure functions, with the `const fn` syntax being
introducted). For declaring variables `Dim::new(value)` can be used. You should never
have to muck with `PhantomData`.

The `base` block is used to define the base units of the system. For example, the line

```rust
Apple, apple, a;
```

defines the type `Apple`, the corresponding constant `apple` (with a value of `1.0`),
and will use the token "a" for printing `Apple`s. The type signature of `apple` is
`Dim<Apple, f64>` and it is this type signature that will be useful for writing
functions that take specific dimensioned quantities. You will probably never want to use
`Apple` by itself.

Note that `Apple` is just a convenient alias for the full type signature, which is given by

```rust
type Apple = Fruit<P1, Zero, Zero, Zero, Zero>;
```

While you should never need to use this signature directly, it will crop up in error
messages, so it's good to be aware of it.

The derived block is currently a placeholder, but will used for naming types and
creating constants for derived units. Here is an example of the intended syntax for when it's implemented,

```rust
mapple: Mapple = Mango * Apple;
```


You can then use it like so

```rust
let fruit_salad = apple * banana * mango * mango * watermelon;
println!("Mmmm, delicious: {}", fruit_salad);
assert_eq!(format!("{}", fruit_salad), "1 a*b*m^2*w");
```

### <a name = "advanced"></a>Advanced macro


If you want a bit more flexibility when creating a unit system, there is a second macro
with a few more options. Here is it used in defining the
[CGS](https://github.com/paholg/dimensioned/blob/master/src/cgs.rs) system:

```rust
mod cgs {
    make_units_adv! {
        CGS, Unitless, one, f64, 1.0;
        base {
            P2, Centimeter, centimeter, cm;
            P2, Gram, gram, g;
            P1, Second, second, s;
        }
        derived {
        }
    }
}
```

The first line

```rust
CGS, Unitless, one, f64, 1.0;
```

is as before, but with two extra items; the type that you wish to use for your defined
constants and the value to initialize them to. Once associated constants arrive, you
will no longer specify the value. Instead, `std::num::One` will be used.

The lines defining base units also each have an extra item. It corresponds to the
highest root that you wish to allow for your units. In almost all cases, it will be
`P1`, the type correspoding to the Peano number of positive one. In the CGS system,
for example, the square root of centimeters and of grams are well-defined, useful units,
so `P2` is used for each of them.

You may use anything from `P1` to `P9`. If for some reason you need something higher,
you can define it as so:

```rust
use dimensioned::{P9, Succ};
type P10 = Succ<P9>;
```

It is quite possible that more features will be added to `make_units_adv!()`, but the
`make_units!()` macro should be fairly stabilized.
