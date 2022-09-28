from pydantic import BaseModel, validator
from itertools import combinations

from .products import Product
from .vehicle import Vehicles


class DeliveryService(BaseModel):
    """
    Model of DeliveryService to handle packaging & dispatching

    Delivery service handling product/item packaging and dispatching of vehicles

    Args:
        package_list (list[Product]): a list of Products for delivery
        transport (Vehicles): vehicles & transport service for the delivery

    Raises:
        ValidationError: If the type validation fails or input doesnot satify the condition
    """

    package_list: list[Product]
    transport: Vehicles

    @validator("transport")
    def __is_transportable(cls, v, values) -> Vehicles:
        # Check if the vehicle is capable of delivering all products.
        # i.e., the vehicle's maximum load must always be greater than any delivery product's weight
        if v is None or not isinstance(v, Vehicles):
            raise ValueError("'transport' should be of type 'Vehicles'")
        for item in values["package_list"]:
            if item.weight > v.max_load:
                raise ValueError(
                    f"Max load capacity of Vehicle is not enough for delivery of a Package({item})"
                )
        return v

    def __summate_package(self, package_list: list[Product], attr: str) -> float:
        # Summation on given attribute of products list
        return sum(package[attr] for package in package_list)

    def get_undelivered_packages(self) -> list[Product]:
        """
        Fetch the undelivered packages out of initial list

        Returns:
            list[Product]: list of products that are not yet delivered
        """
        return [item for item in self.package_list if item.delivered_time == 0]

    def select_packages(self) -> list[Product]:
        """
        Selecting products for delivery

        Selecting a set of packages/products for the certain dispatch made.
        The selection criteria is as below: (order based priority)
            1. Maximum number of packages
            2. Heavier packages
            3. Packages that can be shipped faster
        Currently, Brute-force method is used to find the solution satisfying the need.
        This can be extended as Mixed Integer Programming (MIP problem)
        -- Multi-Objective Multi-bin Knapsack problem
        Google's ORtools can also help in this usecase

        Returns:
            list[Product]: the list of products selected
        """
        packages_count: int = 0
        packages: list = []
        delivery_weight: int = 0
        delivery_distance: int = 0
        undelivered = self.get_undelivered_packages()
        for combo in range(len(undelivered), 0, -1):
            for item_list in combinations(undelivered, combo):
                curr_weight = self.__summate_package(item_list, "weight")
                curr_dist = self.__summate_package(item_list, "destination_distance")
                if curr_weight <= self.transport.max_load:
                    if curr_weight < delivery_weight:
                        continue
                    if curr_weight == delivery_weight and delivery_distance <= curr_dist:
                        continue
                    delivery_distance = curr_dist
                    delivery_weight = curr_weight
                    packages = item_list
                    packages_count = len(item_list)
            if packages_count > 0:
                return packages
        return []

    def deliver(self) -> None:
        """
        Triggers delivery of given Packages/Products

        For every dispatch of vehicle, a set of packages are selected
        for delivery. And the vehicle awaiting on the priority queue is used.
        Once the delivery is dispatced, the Product's estimated delivery time is updated
        """
        decimal_floor = lambda value, precision: ((value * 10**precision) // 1) / 10**precision
        total_pkg: int = len(self.get_undelivered_packages())
        while total_pkg > 0:
            vehicle_time: float = self.transport.next_available()
            max_time: float = 0
            for package in self.select_packages():
                total_pkg -= 1
                package.delivered_time = decimal_floor(
                    vehicle_time + (package.destination_distance / self.transport.speed), 2
                )
                if max_time < package.delivered_time:
                    max_time = package.delivered_time
            self.transport.update_availability(max_time * 2)
