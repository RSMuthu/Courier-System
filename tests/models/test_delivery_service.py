from courier.models import DeliveryService, Product, Vehicles

p1 = Product(name="P1", base_cost=100, offer="OFR001", weight=50, destination_distance=30)
p2 = Product(name="P2", base_cost=100, offer="OFFR0008", weight=75, destination_distance=125)
p3 = Product(name="P3", base_cost=100, offer="OFFR003", weight=175, destination_distance=100)
p4 = Product(name="P4", base_cost=100, offer="OFR002", weight=100, destination_distance=60)
p5 = Product(name="P5", base_cost=100, offer="NA", weight=155, destination_distance=95)
p6 = Product(name="P6", base_cost=100, offer="OFR001", weight=100, destination_distance=50)
p7 = Product(name="P7", base_cost=100, offer="OFR001", weight=100, destination_distance=50)
p8 = Product(name="P8", base_cost=100, offer="OFR001", weight=100, destination_distance=70)
p9 = Product(name="P9", base_cost=100, offer="OFR001", weight=100, destination_distance=30)
p10 = Product(name="P10", base_cost=100, offer="OFR001", weight=110, destination_distance=30)

service: DeliveryService = DeliveryService(
    transport=Vehicles(speed=70, max_load=200, count=2),
    package_list=[p1, p2, p3, p4, p5],
)
service2: DeliveryService = DeliveryService(
    transport=Vehicles(speed=70, max_load=200, count=2),
    package_list=[p6, p7, p8, p9, p10],
)


def test_package_selection_optimised():
    outcome: list[Product] = service.package_selection()
    assert p2 in outcome and p4 in outcome
    outcome2: list[Product] = service2.package_selection()
    assert p6 in outcome2 and p9 in outcome2
    p6.delivered_time = 1
    p9.delivered_time = 1
    outcome3: list[Product] = service2.package_selection()
    assert p7 in outcome3 and p8 in outcome3


def test_package_selection():
    # Legacy
    outcome: list[Product] = service.select_packages()
    assert p2 in outcome and p4 in outcome


def test_package_delivery():
    service.deliver()
    assert 0 == len(service.get_undelivered_packages())
    assert 3 == len(service2.get_undelivered_packages())
    p6.delivered_time = 0
    p9.delivered_time = 0
    service2.deliver()
    assert 0 == len(service2.get_undelivered_packages())
    # Validate delivery
    assert p1.delivered_time == 3.98
    assert p2.delivered_time == 1.78
    assert p3.delivered_time == 1.42
    assert p4.delivered_time == 0.85
    assert p5.delivered_time == 4.19
    assert p6.delivered_time == 0.71
    assert p7.delivered_time == 0.71
    assert p8.delivered_time == 1.0
    assert p9.delivered_time == 0.42
    assert p10.delivered_time == 1.84
