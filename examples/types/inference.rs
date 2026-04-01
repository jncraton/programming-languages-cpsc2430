fn main() {
    let elem = 5u8;
    // The compiler knows that `elem` has type u8

    let mut vec = Vec::new();
    // The compiler doesn't yet know the exact type of `vec`
    // It just knows that it's a vector (`Vec<_>`)

    vec.push(elem);
    // Aha! Now the compiler knows that
    // `vec` is a vector of `u8`s (`Vec<u8>`)

    println!("{:?}", vec);
}