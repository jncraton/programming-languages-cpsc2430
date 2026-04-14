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
