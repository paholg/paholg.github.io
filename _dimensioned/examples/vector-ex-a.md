---
title: Example A
layout: project
project: dimensioned
---

```rust

#[macro_use]
extern crate dimensioned;
use std::ops::{Mul, Div, Add, Sub};
use std::fmt::{self, Display};
use dimensioned::{Dim};
use dimensioned::si::{Unitless};

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

use dimensioned::si::{one, m, kg, s};

impl Mul<Vector3> for f64 {
    type Output = Vector3;
    fn mul(self, rhs: Vector3) -> Vector3 {
        Vector3::new(self*rhs.x, self*rhs.y, self*rhs.z)
    }
}

dim_impl_unary!(Norm2, norm2, Mul, Vector3 => f64);

use dimensioned::{Dimension, Same};
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

dim_impl_binary!(Dot, dot, Mul, Vector3 => f64);
dim_impl_binary!(Cross, cross, Mul, Vector3 => Vector3);

fn main() {

    let xhat = one * Vector3::new(1.0, 0.0, 0.0);

    let yhat: Dim<Unitless, Vector3> = Dim::new(Vector3::new(0.0, 1.0, 0.0));

    3.0*m*xhat + m*yhat;
    13.0*m*xhat;
    2.0*xhat/s;

    let velocity = 3.0*m/s*xhat + 4.0*m/s*yhat;
    let speed = velocity.map(Vector3::norm);
    assert_eq!(speed, 5.0*m/s);

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
}
```