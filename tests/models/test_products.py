from courier.models import Product
from pydantic import ValidationError
import pytest


def test_package_cost():
    package1: Product = Product(
        name="P1", base_cost=100, offer="OFR002", weight=12, destination_distance=2
    )
    assert package1.calculate_total_cost() == 230
    package2: Product = Product(
        name="P2", base_cost=100, offer="OFR001", weight=150, destination_distance=50
    )
    assert package2.calculate_total_cost() == 1665
    package3: Product = Product(
        name="P3", base_cost=100, offer="OFR003", weight=100, destination_distance=150
    )
    assert package3.calculate_total_cost() == 1757.50


def test_package_invalid_data():
    with pytest.raises(ValidationError):
        package4: Product = Product(
            name="P4", base_cost=-100, offer="OFR003", weight=100, destination_distance=150
        )
        package5: Product = Product(
            name="P5", base_cost=100, offer="OFR003", weight=-100, destination_distance=150
        )
        package6: Product = Product(
            name="P6", base_cost=100, offer="OFR003", weight=100, destination_distance=-150
        )
        package7: Product = Product(name="P7", base_cost=100, weight=100, destination_distance=-150)
