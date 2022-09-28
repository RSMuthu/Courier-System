from pydantic import BaseModel, validator
from pydantic.fields import ModelField
from heapq import heappush, heappop

from courier.utils import unsigned_model_validate


class Vehicles(BaseModel):
    """
    Model of Vehicles for delivery service

    There could be n Vehicles on hand and each could go on multiple trips for delivery
    So the vehicles could go & come at different times. To manage the vehicles availability for delivery,
    priority queue (made of Heap) is used, where priority is based on vehicle's next available time

    Args:
        count (int): Number of vehicles
        max_load (float): Maximum load a vehicle can take in (kg)
        speed (float): Speed in which vehicle will always run

    Raises:
        ValidationError: If the type validation fails or input doesnot satify the condition
    """

    count: int
    max_load: float
    speed: float

    # a validator for Model input args
    __validate_attrs = validator("max_load", "speed", allow_reuse=True)(unsigned_model_validate)

    @validator("count", pre=True)
    def __validate_vehicle(cls, count, values, field) -> int:
        # Vehicle count validator
        # As part of vehicle count validation, an array is also created to hold availability information
        unsigned_model_validate(count, field)
        cls.__vehicle_availabile_time = [0 for _ in range(count)]
        return count

    @property
    def vehicle_availabile_time(self) -> list[float]:
        return self.__vehicle_availabile_time

    def next_available(self) -> float:
        """
        Gets next available vehicle's time

        heap pop operation is used for dequeue op

        Returns:
            float | None: next available vehicle's time. None if no vehicle available
        """
        if len(self.__vehicle_availabile_time) == 0:
            return None
        return heappop(self.__vehicle_availabile_time)

    def update_availability(self, time: float) -> None:
        """
        Updates Vehicles availability

        The new time of the vehicles return is added back to priority queue
        Heap push op is used for enqueue op

        Args:
            time (float): the new time for the vehicle to be added to priority queue

        """
        heappush(self.__vehicle_availabile_time, time)
