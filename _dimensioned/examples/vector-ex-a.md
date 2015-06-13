---
title: Example A
layout: project
project: dimensioned
---

```rust
#[macro_use]
extern crate dimensioned;
use std::ops::{Mul};
use dimensioned::{Dim};
use dimensioned::si::{Unitless};
#[derive(Copy, Clone, PartialEq, PartialOrd)]
pub struct Vector3 {
    x: f64,
    y: f64,
    z: f64,
}

impl Vector3 {
    fn new(x: f64, y: f64, z: f64) -> Vector3 {
        Vector3{ x: x, y: y, z: z}
    }
    fn cross(self, rhs: Vector3) -> Vector3 {
        Vector3{ x: self.y*rhs.z - self.z*rhs.y,
                 y: self.z*rhs.x - self.x*rhs.z,
                 z: self.x*rhs.y - self.y*rhs.x }
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
use dimensioned::si::{one, m, kg, s};
impl Mul<Vector3> for f64 {
    type Output = Vector3;
    fn mul(self, rhs: Vector3) -> Vector3 { Vector3::new(self*rhs.x, self*rhs.y, self*rhs.z) }
}

fn main() {
    let xhat = one * Vector3::new(1.0, 0.0, 0.0);
    let yhat: Dim<Unitless, Vector3> = Dim::new(Vector3::new(0.0, 1.0, 0.0));
}
```