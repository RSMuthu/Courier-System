from courier.models import Offer


def test_offer_validity():
    offer1: Offer = Offer(offer_code="OFR001")
    assert offer1.is_valid() == True
    offer2: Offer = Offer(offer_code="test")
    assert offer2.is_valid() == False
    offer3: Offer = Offer()
    assert offer3.is_valid() == False
    offer4: Offer = Offer(offer_code=None)
    assert offer4.is_valid() == False


def test_discount_amount():
    offer1: Offer = Offer(offer_code="OFR003")
    assert offer1.get_discount(75, 249) == 5
    offer2: Offer = Offer(offer_code="test")
    assert offer2.is_valid() == 0
    offer3: Offer = Offer()
    assert offer3.is_valid() == 0
    offer4: Offer = Offer(offer_code=None)
    assert offer4.is_valid() == 0
    offer5: Offer = Offer(offer_code="OFR002")
    assert offer5.get_discount(150, 50) == 7
    offer6: Offer = Offer(offer_code="OFR001")
    assert offer6.get_discount(99, 1) == 10
