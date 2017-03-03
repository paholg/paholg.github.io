---
title: Dimensioned 0.6.0
layout: post
---

Dimensioned, the Rust library that I have written for compile-time dimensional analysis, has just
reached version 0.6.0! This version change indicates a full rewrite of the library, and I think
that it has made it much more usable.

I first started this crate before Rust had hit 1.0, and I fairly quickly realized that what I
wanted was not possible. With the advent of associated types, it became possible, and two years ago
I first announced its existence. It was really a proof of concept at that point; it was lacking in
ergonomics and some pretty important features.

Today, I am excited to report that I believe it is more than a proof of concept, and is ready to be
used.

Here are some notable changes:

* No longer do we need a nightly compiler! Dimensioned now works fine on Rust stable, so long as it
  is at least version 1.15.
* Before, units were expressed by parametrizing a `Dim` struct. That struct is gone, which brings a
  couple benefits. The first is ergonomics; a meter was expressed as `Dim<Meter, V>` in past
  verions, and now it is `Meter<V>`. The second benefit is in Rust's orphan rules; if you create a
  unit system, you now create the outermost struct, and so have full control over what you can
  implement for it.
* We no longer depend on `std`! Use dimensioned wherever you desire!
* Thanks to type macros, derived units can now be defined without a build script or the *extremely*
  clunky syntax that was necessary before.
* Unit systems! We have added unit systems and definitions for many derived units and
  constants. They are still incomplete, though, and an area where dimensioned should improve on
  soon.

If you have some time, check out the
[documentation](http://paholg.com/dimensioned/dimensioned/index.html), or the
[readme](https://github.com/paholg/dimensioned). I have tried to make these documents as clear and
comprehensive as possible, but I am sure that I have failed in at least some ways.

Please feel free to submit an [issue on GitHub](https://github.com/paholg/dimensioned/issues) or
leave a comment on [reddit](https://www.reddit.com/r/rust/comments/5x9jgq/dimensioned_06_compiletime_dimensional_analysis/) or on the [Rust user's forum](https://users.rust-lang.org/t/dimensioned-0-6-compile-time-dimensional-analysis-much-nicer-than-before/9759).
