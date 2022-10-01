from courier.models import DeliveryService, Product, Vehicles

p1 = Product(name="P1", base_cost=100, offer="OFR001", weight=50, destination_distance=30)
p2 = Product(name="P2", base_cost=100, offer="OFFR0008", weight=75, destination_distance=125)
p3 = Product(name="P3", base_cost=100, offer="OFFR003", weight=175, destination_distance=100)
p4 = Product(name="P4", base_cost=100, offer="OFR002", weight=100, destination_distance=60)
p5 = Product(name="P5", base_cost=100, offer="NA", weight=155, destination_distance=95)

service: DeliveryService = DeliveryService(
    transport=Vehicles(speed=70, max_load=200, count=2),
    package_list=[p1, p2, p3, p4, p5],
)


def test_package_selection():
    outcome: list[Product] = service.select_packages()
    assert p2 in outcome and p4 in outcome


def test_package_delivery():
    service.deliver()
    assert 0 == len(service.get_undelivered_packages())
