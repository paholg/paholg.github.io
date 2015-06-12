initSidebarItems({"struct":[["Dim","This is the primary struct that users of this library will interact with."]],"trait":[["Cbrt","Because it would not make sense to implement `Float` for `Dim<D, V>`, we create a special `Cbrt` trait. We then implement it for `Dim<D, V>` where `V: Float`"],["DimToString","This trait gives a human-friendly representation of a dimensioned object. It is useful for printing and debugging."],["Dimension","All types created for a unit system will implement this trait."],["Dimensionless","The only types that implement this trait are the `Unitless` types that exist in each unit system. It allows more flexibility when handling specifically objects without dimension."],["DivDim","This trait allows us to divide two dimensioned objects"],["InvertDim","This trait inverts the dimensions of an object. For example, it takes seconds to hertz."],["KeepDim","This trait enforces that `Self` and `RHS` have the same dimensions. It is useful mostly for macros."],["MulDim","This trait allows us to multiply two dimensioned objects"],["NotDim","This traits is implemented by default for everything that is not Dim<D, V>. It allows a greater level of generic operator overloading than would be possible otherwise."],["Pow","Generic integer powers using peano numbers. No other types should implement it. Example: ``` let x = 2.0*m; assert_eq!(x*x, Two::pow(x)); ```"],["PowerDim","This trait allows us to take a dimensioned object to a power given by a peano number"],["Root","Generic roots using peano numbers. No other types should implement it. # Example ``` use dimensioned::si::m; use dimensioned::Root; use dimensioned::peano::Two;"],["RootDim","This trait allows us to take a root, given by a peano number, of a dimensioned object"],["Sqrt","Because it would not make sense to implement `Float` for `Dim<D, V>`, we create a special `Sqrt` trait. We then implement it for `Dim<D, V>` where `V: Float`"]]});