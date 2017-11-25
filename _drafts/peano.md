---
title: Learning to count
subtitle: Playing with Rust's type system, part 1
layout: post
---

The Rust language has a fantastic type system, and I have had a lot of fun pushing it to its
limits. So let's do a bit of that here.

One feature that Rust lacks is type-level integers. Numbers that are evaluated at compile time and
can be used as part of type signatures can be very useful, and they do crop up one place in Rust:
arrays. Arrays have type `[T; N]` where `T` is some type and `N` is a number. Fantastic! Only we
can never be generic over those numbers and we can never use them in our own types.

If I want to write a trait for arrays, then I have to implement it for every possible length. This
is a real issue, and it crops up even in the standard library. Take a look
[here](https://doc.rust-lang.org/std/primitive.array.html#implementations). Each trait is
implemented for every array size up to 32. Arrays larger than 32 elements are really second class
citizens.

Furthermore, say you want to write a linear algebra library, and for performance and type-safety
reasons, you want the dimensions of matrices to be encoded in their types. Something like this:

```rust
struct Matrix<T, N, M> {
    data: [[T; N]; M],
}
```

You can't do it!

This is a feature desired by enough of the community that I imagine it will make it into the
language some day. I say "Humbug!" to "some day" though, I want it now!

Okay, so let's make our own type-level numbers. We're going to take motivation from the
[Peano axioms](https://en.wikipedia.org/wiki/Peano_axioms) which is what mathematicians use to
construct the natural numbers.

First, we have: `0 is a natural number`. The name `0` isn't special (yet), basically we're just
saying that a natural number exists, and we're going to call it `0`. Great, we can do that:

```rust
enum Zero;
```

That was easy! Note that we have made `Zero` and empty enum rather than a struct. Were it a struct,
then one could do something like `let x = Zero;` and create an object out of it. We don't want that;
these numbers should only ever appear in types. No one can create an object out of an enum that has
no variants, though, so we're off the hook.

It will be nice to have a trait to which all of our numbers will belong; let's call it `Peano`.

```rust
trait Peano;
impl Peano for Zero {}
```

Okay, that was easy, what's next? A bunch of stuff that boils down to "equality is a thing, and it
works how you think it should". The compiler handles this for us. Rust would have to have a pretty
poor and bizarre type system for it not to.

Now we get to define more numbers. For each natural number *n*, the *S(n)* is also a natural number
where *S(n)* is the "successor" function. Essentially, we can count, and we can always count up. In
code, this looks like:

```rust
struct<N: Peano> Succ<N> {
    _marker: PhantomData<N>,
}

impl<N: Peano> Peano for Succ<N> {}
```

Rust forces us to use any type parameters we take, so the `PhantomData` is there to say "I'm using
`N`, but I'm just not doing anything with it. It's okay."

Well, we're done. We now have types that correspond to all natural numbers, and we can use them
generically or specifically. Yay. We can even use type aliases to name some of them:

```rust
type P1 = Succ<Zero>;
type P2 = Succ<P1>;
type P3 = Succ<P2>;
⋮
```

In truth, we don't have all natural numbers. By default, Rust only allows 64 nested types, meaning
we can only count to 63. That limit can be increased, but the type system isn't really designed for
that and it can bog things down. Fortunately, there's a more efficient encoding of numbers, and
it's the one computers already use: binary. It is outside the scope of this post, but
[typenum](https://crates.io/crates/typenum/) uses a binary encoding of types to achieve this
result. Check it out if you have a use for type-level numbers, or are just curious how it goes
about it.

Anyway, we have defined the natural numbers. For the vast majority of use cases, that is
sufficient. Not for me, though. I want not just natural numbers, but all integers, and I want to be
able to perform arithmetic.

We can achieve the former by counting down, in addition to up, with a predecessor type,
`Pred<N>`. We have to be careful, though. If we end up with, say, `Succ<Pred<Zero>>` then that's
conceptually equal to `Zero`, but the type system sees it as a distinct type, so we have broken the
equality axioms that I glossed over. Uh oh!

Let's make two more traits, to keep track of what kinds of numbers we have. Because they're about
our type numbers, only things that belong to `Peano` should belong to them.

```rust
trait NonNeg: Peano;
trait NonPos: Peano;
```

I have named them that way so that they can both include `Zero`:

```rust
impl NonNeg for Zero {}
impl NonPos for Zero {}
```

And now let's slightly change the definition of our successor type:

```rust
struct<N: NonNeg> Succ<N> {
    _marker: PhantomData<N>,
}
impl<N: NonNeg> NonNeg for Succ<N> {}
```

So, we can only use our successor for things that aren't negative. Let's similarly define a
predecessor type:

```rust
struct<N: Peano + NonNeg> Succ<N> {
    _marker: PhantomData<N>,
}
```
