---
title: Creating a unit system
layout: project
project: dimensioned
---

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

use dimensioned::{Dim};
use fruit::Unitless;
use std::marker::PhantomData;
pub const one: Dim<Unitless, f64> = Dim(1.0, PhantomData);

use fruit::Fruit;
use dimensioned::{Zero, P1};
type Apple = Fruit<P1, Zero, Zero, Zero, Zero>;

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

use dimensioned::{P9, Succ};
type P10 = Succ<P9>;

fn main() {

    let fruit_salad = apple * banana * mango * mango * watermelon;
    println!("Mmmm, delicious: {}", fruit_salad);
    assert_eq!(format!("{}", fruit_salad), "1 a*b*m^2*w");
}
```