fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

fn main() {
  match divide(2.0, 1.0) {
      Some(x) => println!("Result: {}", x),
      None    => println!("Cannot divide by 0"),
  }

  match divide(2.0, 0.0) {
      Some(x) => println!("Result: {}", x),
      None    => println!("Cannot divide by 0"),
  }
}
