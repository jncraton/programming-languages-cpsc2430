---
reading: 'Chapter 10: Object-Oriented Programming'
...

# Final Exam

---

![Exam Schedule](https://anderson.edu/wp-content/uploads/ExamSchedule20252026.pdf)

# Object-Oriented Programming

## Abstraction

- Allows us to hide complexity behind simpler interfaces

## Data Abstraction

- Create complex data structures with simple interfaces to pass around (e.g. records, structs, dictionaries, etc)

## Control Abstraction

- Create organized sections of executable code that execute in well-understood ways and can be reused

## Classes

- Allow programmers to define a group of related abstractions (objects)
- Programming techniques built around classes are considered object-oriented
- Combine control and data abstraction

## Data Members

- Provide data abstraction
- Hold data used by objects
- Also known as `fields` or `properties`

## Subroutine Members

- Provide control abstraction
- Subroutines and functions that objects can run
- Also known as `methods`

## Constructors

- Called to instantiate class object

---

```python
class Asset():
  def __init__(self, value, appreciation=.05, maintenance=.02):
    self.value = value
    self.appreciation = appreciation
    self.maintenance = maintenance
```

## `this` and `self`

- Provide explicit reference to class instance

## Why Classes?

- We can define new abstractions as extensions or refinements of existing abstractions via inheritance

## Liskov Substitution Principle

> Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.

## Inheritance Example

```python
class Asset:
    """
    Represents some asset and provides methods to operate on it

    >>> bitcoin = Asset(1, appreciation=1)
    >>> int(bitcoin.future_value(years=10))
    1024
    >>> int(bitcoin.change_in_value(years=10))
    1023
    """

    def __init__(self, value, appreciation):
        self.value = value
        self.appreciation = appreciation

    def future_value(self, years):
        return self.value * (1 + self.appreciation) ** years

    def change_in_value(self, years):
        return self.future_value(years) - self.value


class House(Asset):
    """ Represents a real estate asset

    >>> house = House(100000, appreciation=.01, maintenance=.02, tax=.03, utilities=100)
    >>> int(house.operating_cost(10))
    53311

    >>> int(house.tco(10))
    42848
    """

    def __init__(self, value, appreciation=0.02, maintenance=0.02, tax=0.01, utilities=200):
        super().__init__(value, appreciation)
        self.maintenance = maintenance
        self.tax = tax
        self.utilities = utilities

    def operating_cost(self, years):
        maintenance = sum(self.future_value(y) * self.maintenance for y in range(years))
        tax = sum(self.future_value(y) * self.tax for y in range(years))
        return maintenance + tax + self.utilities * years

    def tco(self, years):
        return -self.change_in_value(years) + self.operating_cost(years)


class Vehicle(Asset):
    """
    Represents a vehicle of some type

    >>> car = Vehicle(16000, appreciation=-.2, maintenance=500, mpg=22)
    >>> int(car.tco(years=5))
    20075
    >>> car = Vehicle(16000, appreciation=-.2, maintenance=500, mpg=38)
    >>> int(car.tco(years=5))
    17204
    """

    def __init__(self, value=16000, appreciation=-0.25, maintenance=300, mpg=25):
        super().__init__(value, appreciation)
        self.maintenance = maintenance
        self.mpg = mpg

    def operating_cost(self, years, miles_per_year=10000, gas_price=3.0):
        return self.maintenance * years + miles_per_year / self.mpg * gas_price * years

    def tco(self, years):
        return -self.change_in_value(years) + self.operating_cost(years)

if __name__ == '__main__':
    house = House(100000, appreciation=0.04, tax=.01, maintenance=.02)
    print("House", house.tco(10))

    car = Vehicle(35000, appreciation=-0.20, mpg=22)
    print("Car", car.tco(10))

    car = Vehicle(8000, appreciation=-0.10, mpg=35)
    print("Budget car", car.tco(10))
```

---

Favor composition over inheritance

## Inheritance

- Represents an **is-a** relationship
- Encourages chains of inheritance and attempting to fit arbitrary problems into an inheritance model

## Composition

- Represents a **has-a** relationship
- Encourages combining multiple classes as members of one another

## Rust Trait Example

```rust
struct Asset<T> {
  value: f64,
  appreciation: f64,
  costs: T,
}

impl<T> Asset<T> {
  fn future_value(&self, years: u32) -> f64 {
    self.value * (1.0 + self.appreciation).powi(years as i32)
  }

  fn change_in_value(&self, years: u32) -> f64 {
    self.future_value(years) - self.value
  }
}

trait OperatingCost {
  fn calculate(&self, asset_value: f64, appreciation: f64, years: u32) -> f64;
}

struct HouseCosts {
  maintenance_rate: f64,
  tax_rate: f64,
  utilities: f64,
}

impl OperatingCost for HouseCosts {
  fn calculate(&self, asset_value: f64, appreciation: f64, years: u32) -> f64 {
    let mut total = 0.0;
    for y in 0..years {
      let current_val = asset_value * (1.0 + appreciation).powi(y as i32);
      total += current_val * (self.maintenance_rate + self.tax_rate);
    }
    total + (self.utilities * years as f64)
  }
}

struct VehicleCosts {
  annual_maintenance: f64,
  mpg: f64,
}

impl OperatingCost for VehicleCosts {
  fn calculate(&self, _asset_value: f64, _appreciation: f64, years: u32) -> f64 {
    let miles_per_year = 10000.0;
    let gas_price = 3.0;
    let annual_gas = (miles_per_year / self.mpg) * gas_price;
    (self.annual_maintenance + annual_gas) * years as f64
  }
}

impl<T: OperatingCost> Asset<T> {
  fn total_cost_of_ownership(&self, years: u32) -> f64 {
    let costs = self.costs.calculate(self.value, self.appreciation, years);
    -self.change_in_value(years) + costs
  }
}

fn main() {
  let house_asset = Asset {
    value: 100000.0,
    appreciation: 0.04,
    costs: HouseCosts {
      maintenance_rate: 0.02,
      tax_rate: 0.01,
      utilities: 200.0,
    },
  };

  let car_asset = Asset {
    value: 35000.0,
    appreciation: -0.20,
    costs: VehicleCosts {
      annual_maintenance: 300.0,
      mpg: 22.0,
    },
  };

  let budget_car_asset = Asset {
    value: 8000.0,
    appreciation: -0.10,
    costs: VehicleCosts {
      annual_maintenance: 300.0,
      mpg: 35.0,
    },
  };

  println!("House TCO: {}", house_asset.total_cost_of_ownership(10));
  println!("Car TCO: {}", car_asset.total_cost_of_ownership(10));
  println!("Budget Car TCO: {}", budget_car_asset.total_cost_of_ownership(10));
}
```
