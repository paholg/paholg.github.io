initSidebarItems({"struct":[["UInt","UInt is defined recursevly, where B is the least significant bit and U is the rest of the number. U can be another UInt or UTerm. In order to keep numbers unique, leading zeros are not allowed, so `UInt<UTerm, B0>` should never show up anywhere ever."],["UTerm","The terminating type for `UInt`, it always comes after the most significant bit."]],"trait":[["Unsigned","This trait is implemented for the all things that a `UInt` can take as a parameter, which is just `UInt` and `UTerm` (used to terminate the `UInt`). It should not be implemented for anything outside this crate."]]});