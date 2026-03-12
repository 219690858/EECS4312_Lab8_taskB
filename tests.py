import pytest
from solution import EventRegistration, UserStatus, DuplicateRequest, NotFound


# Covers C1, AC1
def test_register_until_capacity_then_waitlist():
    er = EventRegistration(capacity=1)

    er.register("u1")
    status = er.register("u2")

    assert status == UserStatus("waitlisted", 1)


# Covers C3, AC3
def test_waitlist_fifo_order():
    er = EventRegistration(capacity=1)

    er.register("u1")
    er.register("u2")
    er.register("u3")

    assert er.status("u2") == UserStatus("waitlisted", 1)
    assert er.status("u3") == UserStatus("waitlisted", 2)


# Covers C1, AC1 (Edge Case)
def test_waitlist_promotion_after_cancel():
    er = EventRegistration(capacity=1)

    er.register("u1")
    er.register("u2")

    er.cancel("u1")

    assert er.status("u2") == UserStatus("registered")


# Covers C5, AC5 (Edge Case)
def test_duplicate_registration_rejected():
    er = EventRegistration(capacity=1)

    er.register("u1")

    with pytest.raises(DuplicateRequest):
        er.register("u1")


# Covers C5, AC7 (Edge Case)
def test_cancel_nonexistent_user():
    er = EventRegistration(capacity=1)

    with pytest.raises(NotFound):
        er.cancel("missing")


# Covers C8, AC8
def test_deterministic_behavior():
    er1 = EventRegistration(1)
    er2 = EventRegistration(1)

    er1.register("u1")
    er1.register("u2")

    er2.register("u1")
    er2.register("u2")

    assert er1.snapshot() == er2.snapshot()