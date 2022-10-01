from pydantic import BaseModel

import json

with open("./offers_config.json", 'r') as json_obj:
    OFFERS = json.load(json_obj)

class Offer(BaseModel):
    """
    Model of Offer for the products

    This holds the set of applicable offers and
    handles necessary processing for the Offers

    Args:
        offer_code (str): the offer code name

    Raises:
        ValidationError: If the type validation fails or input doesnot satify the condition
    """

    offer_code: str = None

    def __validate_offer_conditions(self, weight: float, distance: float) -> bool:
        # check the different requirements of selected offer code
        # against the products' data
        weight_range = OFFERS[self.offer_code]["weight_range"]
        distance_range = OFFERS[self.offer_code]["distance_range"]
        return (
            weight_range["min"] <= weight <= weight_range["max"]
            and distance_range["min"] <= distance <= distance_range["max"]
        )

    def is_valid(self) -> bool:
        """
        Offer Validator

        Checks and validates against the list of offer codes available

        Returns:
            bool: based on validity
        """
        return self.offer_code in OFFERS

    def get_discount(self, weight: float, distance: float) -> float:
        """
        Get discount ammount for offer applied

        Return the discount amount for the product after all the validations

        Args:
            weight (float): product's weight
            distance (float): product's delivery distance

        Returns:
            float: total discount amount
        """
        if self.is_valid() and self.__validate_offer_conditions(weight, distance):
            return OFFERS[self.offer_code]["discount"]
        return 0
