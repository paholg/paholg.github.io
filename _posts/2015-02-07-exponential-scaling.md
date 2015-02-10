---
title: Compile scaling
layout: post
name: compile
---

I am working on a Rust library, Dimensioned, that implements compile-time type checking
of arbitrary unit systems using Rust's type system, and I have noticed an oddity.

To start, I have implemented the Peano numbers. While the full implementation can be
found [here](https://github.com/paholg/dimensioned/blob/master/src/peano.rs), here are the relevant
bits:

{% highlight rust %}
pub struct Zero;
pub struct Succ<T: NonNeg>;

pub trait AddPeano<RHS = Self> {
    type Output;
}
/// Adding things to zero (e.g. 0 + 3)
impl<RHS: Peano> AddPeano<RHS> for Zero {
    type Output = RHS;
}
/// Adding positive numbers (e.g. 1 + 2)
impl<T: NonNeg + AddPeano<Succ<RHS>>, RHS: NonNeg> AddPeano<Succ<RHS>> for Succ<T> {
    type Output = Succ<<T as AddPeano<Succ<RHS>>>::Output>;
}
{% endhighlight %}

Essentially, in math language, we define the number \\(0\\), and the successor operation
\\(N'\\). If \\(N\\) is a number, then so is \\(N'\\) (mathematically---when programming, there is an upper bound).

Then, we define addition inductively as

$$
  \begin{align*}
  0 + N &= N\\
  N' + M' &= (N + M')'
  \end{align*}
$$

The reason why \\(M'\\) is used instead of \\(M\\) is to differentiate negative and
positive numbers---there is also a predecesor operation, and we want to be sure to never
use them both at the same time. But that isn't really relevant here.

What is relevent is that this is all mostly okay so far. A simple test program on my
computer takes about .85 s to compile and run a test that adds One and One, and about
1.5 s for a test that does repeated adds to get to 63, which currently the maximum
number of nested structs that Rust allows, and so the highest number that my Peano
library supports.

That's not great scaling, but it's not terrible seeing as high numbers are never really
expected and any given operation is only performed once, at compile time.

Now, I am using these Peano numbers to track the powers of various units in an arbitrary
unit system. For simplicity, let's make a basic unit system, `U`, with only one unit,
`Unit`. If we want to multiply two values in this unit system, then we will want to add
the powers of their dimensions which we can do as follows:

{% highlight rust %}
pub trait AddDim<RHS = Self>: Dimension {
  type Output;
}
impl<Unit1, Unit2> AddDim<U<Unit2>> for U<Unit1>
  where Unit1: PInt + AddPeano<Unit2>, Unit2: PInt {
    type Output = U<<Unit1 as AddPeano<Unit2>>::Output>;
}
{% endhighlight %}


And, to actually use this, we wrap it in a new type

{% highlight rust %}
pub struct Dim<T: Dimension, V>(pub V);
{% endhighlight %}


where `U` belongs to our `Dimension` trait and `V` is any type we want. We define the
`Mul` trait for `Dim` as returning an output with the new units embedded in the type
signature (using `AddDim`), and value given by the product of the two `V`-type objects.

Then, we can define a basic unit as:

{% highlight rust %}
pub type Unit = U<Succ<Zero>>;
pub static unit: Dim<Unit, f64> = Dim(1.0);
{% endhighlight %}

Typically, we would have more base units, but this system is just here for
demonstration.

Now, let's run a simple test as follows:

{% highlight rust %}
fn main() {
  let x = unit;

  let y = x*x*x*x*x*x*x;
}
{% endhighlight %}

I would expect this to take about as long to compile as the addition test. After all,
it's just a few thin wrappers around the `AddPeano` trait. but it
doesn't. In fact, multiplying by more and more `x`s scales exponentially.

<img align="center" src="/imgs/time-test.svg" alt="Exponential Plot">
