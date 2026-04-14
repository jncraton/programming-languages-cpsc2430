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
