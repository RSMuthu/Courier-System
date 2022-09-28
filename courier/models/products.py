from pydantic import BaseModel, validator
from .offers import Offer
from courier.utils import unsigned_model_validate


class Product(BaseModel):
    """
    Model of Product which handles cost estimation works

    The Product model holds info about a certain product;
    its cost, weight, delivery distance, offer, etc.
    and helps in calculating the estimated cost

    Args:
        name (str): name of the product
        base_cost (float): product base delivery cost
        weight (float): Product's weight
        destination_distance (float): delivery distance of the given product
        offer (str): string representing offer code

    Raises:
        ValidationError: If the type validation fails or input doesnot satify the condition
    """

    name: str
    base_cost: float
    weight: float
    destination_distance: float
    offer: Offer
    delivered_time: float = 0

    # validator for Model input args
    __validate_attrs = validator("weight", "destination_distance", "base_cost", allow_reuse=True)(
        unsigned_model_validate
    )

    def __str__(self):
        return f"{self.name} {self.__discount} {self.calculate_total_cost()} {self.delivered_time}"

    def __getitem__(self, item: str):
        return getattr(self, item)

    @validator("offer", pre=True)
    def __offer_pre_validate(cls, v, values) -> Offer:
        # validate the input string of offer code
        # and then converts it to instance of Offer & sets the discount value
        if v is not None and not isinstance(v, str):
            raise ValueError("Offer should be string or None")
        return Offer(offer_code=v)

    def __delivery_cost(self) -> float:
        # Calculate base delivery cost
        # Given Logic: Base Delivery Cost + (Package Weight * 10) + (Delivery Distance * 5)
        return self.base_cost + (self.weight * 10) + (self.destination_distance * 5)

    def discount(self) -> float:
        """
        discount percent for the product

        Based on Offer validity & criteria, applicable discount percentage is returned

        Returns:
            float: discount percentage
        """
        return self.offer.get_discount(self.weight, self.destination_distance)

    def calculate_total_cost(self) -> float:
        """
        Calculate total cost of product delivery

        This is calculated with consideration to
        base cost, weight, distance and offer applied

        Returns:
            float: total cost
        """
        d_cost: float = self.__delivery_cost()
        return d_cost - (d_cost * self.discount() / 100)
