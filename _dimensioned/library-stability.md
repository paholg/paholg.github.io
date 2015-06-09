---
title: Library stability
layout: project
project: dimensioned
nav: [[Planned features, planned], [Rust unstable, rustunstable]]
date: 2015-6-8
version: 0.2.2
---

There are two sides to this; dimensioned is still undergoing breaking changes and it
relies on features of unstable Rust.

The main reason dimensioned still has breaking changes is that I have not fully settled
on the interface for some commands.

### <a name="planned"></a> Planned features

I have some more features planned for dimensioned, but I believe I can implement all of
them in a backwards compatible way. Here they are. Let me know if you think I should add
any others!

- Naming derived units: This will be added to the `make_units!` macro, and there is
  already a reserved block for it in the macro.

- Coherence improvements: There are multiple ideas floating around for opening up some of
  Rust's coherence rules. As this happens, it should only make dimensioned more general
  and more easily useable.

- Helper macros: Dimensioned exports a couple macros ([see
  here](work-with-others.html#ExampleA)) to make it easy to use with other types. It may
  be nice to add more.

- Std traits: I have implemented some traits from std and num for dimensioned, but I would
  like to implement all that make sense. Most notably, I have not finished implementing
  `Float` for dimensionless dimensioned objects.


### <a name="rustunstable"></a>Rust unstable

The other issue holding dimensioned back from stabilizing is that it depends on some
unstable features of Rust and I would very much like it to depend on some features that
don't yet exist.

- [Opt-in built-in traits](https://github.com/rust-lang/rfcs/blob/master/text/0019-opt-in-builtin-traits.md): Dimensioned makes use of the syntax `impl Trait for .. {}`,
  which is currently an unstable feature. It allows a higher degree of generic operator
  overloading than would be possible without it, and is fairly essential to the goal of
  making the use of dimensioned as painless as possible.

- [Mutually exclusive traits](https://github.com/rust-lang/rfcs/pull/1148): This is
  currently an RFC, but its implementation would be cleaner than using the default impls
  from opt-in built-in traits.

- [Procedural macros](https://doc.rust-lang.org/book/compiler-plugins.html): While
  declaring derived units is not implemented yet, I am fairly sure that it will require
  procedural macros.

- Other: Anything else that is added to Rust that will aid in generic programming, such
  as type specialization, will likely be incorporated into dimensioned.

The ability to declare default traits is pretty important to dimensioned's function, at
least until there's something better. Once it becomes a stable feature, I will work hard
get dimensioned running on Rust stable.
