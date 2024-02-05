from collections import namedtuple
from pytest import fixture, raises
from symplyphysics import (
    assert_approx,
    errors,
    units,
    convert_to,
    Quantity,
    SI,
)
from symplyphysics.laws.hydro import velocity_from_height as torricellis_formula

# Description
## In the bottom of water tank there is a small hole. Height of liquid in tank is 3m. Velocity of jet according to Torricelli's formula should be
## 7.67m/s


@fixture(name="test_args")
def test_args_fixture():
    h = Quantity(3 * units.meter)
    Args = namedtuple("Args", ["h"])
    return Args(h=h)


def test_basic_velocity(test_args):
    result = torricellis_formula.calculate_velocity(test_args.h)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.velocity)
    result_velocity = convert_to(result, units.meter / units.second).evalf(5)
    assert_approx(result_velocity, 7.67)


def test_bad_height():
    hb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        torricellis_formula.calculate_velocity(hb)
    with raises(TypeError):
        torricellis_formula.calculate_velocity(100)
