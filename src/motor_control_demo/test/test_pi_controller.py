import pytest

from motor_control_demo.pi_controller import PIController


def test_proportional_response():
    controller = PIController(kp=2.0, ki=0.0, output_limit=12.0)
    assert controller.update(error=3.0, dt=0.1) == pytest.approx(6.0)


def test_output_is_saturated():
    controller = PIController(kp=10.0, ki=1.0, output_limit=12.0)
    assert controller.update(error=3.0, dt=0.1) == pytest.approx(12.0)
    assert controller.integral == pytest.approx(0.0)


def test_integral_accumulates():
    controller = PIController(kp=0.0, ki=2.0, output_limit=12.0)
    controller.update(error=1.0, dt=0.5)
    assert controller.update(error=1.0, dt=0.5) == pytest.approx(2.0)


def test_invalid_timestep_is_rejected():
    controller = PIController(kp=1.0, ki=1.0, output_limit=12.0)
    with pytest.raises(ValueError):
        controller.update(error=1.0, dt=0.0)
