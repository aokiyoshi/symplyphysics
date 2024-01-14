from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    Quantity,
    convert_to,
)
from symplyphysics.laws.thermodynamics import speed_of_sound


# Description
# Input: Air, temperatur=20°C, gamma=1.4, M=29 g/mol
# Comparing with the tabular value from Wikipedia
# It should be 343.21 m/s


@fixture(name="test_args")
def test_args_fixture():
    t = Quantity(293.15 * units.kelvin)
    gamma = 1.4
    M = Quantity(29 * units.gram / units.mole)
    Args = namedtuple("Args", ["t", "gamma", "M"])
    return Args(t=t, gamma=gamma, M=M)


def test_speed_of_sound(test_args):
    result = speed_of_sound.calculate_speed_of_sound(
        test_args.t, test_args.gamma, test_args.M)
    result_velocity = convert_to(result, units.meter / units.second).evalf(4)
    assert result_velocity == approx(343.21, 0.01)


def test_bad_temperature(test_args):
    tb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        speed_of_sound.calculate_speed_of_sound(
            test_args.t, test_args.gamma, tb)
    with raises(TypeError):
        speed_of_sound.calculate_speed_of_sound(
            test_args.t, test_args.gamma, 100)


def test_bad_mole_mass(test_args):
    Mb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        speed_of_sound.calculate_speed_of_sound(
            test_args.t, test_args.gamma, Mb)
    with raises(TypeError):
        speed_of_sound.calculate_speed_of_sound(
            test_args.t, test_args.gamma, 100)
