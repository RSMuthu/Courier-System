from courier.models import Vehicles


def test_vehicles_usage():
    transport: Vehicles = Vehicles(speed=70, max_load=200, count=3)
    assert transport.next_available() == 0
    assert transport.next_available() == 0
    assert transport.next_available() == 0
    transport.update_availability(5)
    transport.update_availability(2)
    transport.update_availability(10)
    transport.update_availability(1)
    assert transport.next_available() == 1
    assert transport.next_available() == 2
    assert transport.next_available() == 5
    assert transport.next_available() == 10
