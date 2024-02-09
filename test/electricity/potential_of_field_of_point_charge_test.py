from collections import namedtuple
from pytest import fixture, raises
from symplyphysics import (assert_equal, units, Quantity, errors)
from symplyphysics.laws.electricity import potential_of_field_of_point_charge as potential_law

# Description
## For an electron at a distance of 1 meter, the field potential will be 1.439e-6 volts.
## https://www.calculatoratoz.com/ru/electrostatic-potential-due-to-point-charge-calculator/Calc-578

Args = namedtuple("Args", ["relative_permittivity", "distance", "charge"])


@fixture(name="test_args")
def test_args_fixture() -> Args:
    relative_permittivity = 1
    distance = Quantity(1 * units.meter)
    charge = Quantity(1.6e-16 * units.coulomb)
    return Args(relative_permittivity=relative_permittivity, distance=distance, charge=charge)


def test_basic_electrostatic_potential(test_args: Args) -> None:
    result = potential_law.calculate_electrostatic_potential(test_args.relative_permittivity,
        test_args.distance, test_args.charge)
    assert_equal(result, 1.439e-6 * units.volt)


def test_bad_relative_permittivity(test_args: Args) -> None:
    relative_permittivity = Quantity(1 * units.joule)
    with raises(errors.UnitsError):
        potential_law.calculate_electrostatic_potential(relative_permittivity, test_args.distance,
            test_args.charge)
    with raises(TypeError):
        potential_law.calculate_electrostatic_potential(True, test_args.distance, test_args.charge)


def test_bad_distance(test_args: Args) -> None:
    distance = Quantity(1 * units.joule)
    with raises(errors.UnitsError):
        potential_law.calculate_electrostatic_potential(test_args.relative_permittivity, distance,
            test_args.charge)
    with raises(TypeError):
        potential_law.calculate_electrostatic_potential(test_args.relative_permittivity, 100,
            test_args.charge)


def test_bad_charge(test_args: Args) -> None:
    charge = Quantity(1 * units.joule)
    with raises(errors.UnitsError):
        potential_law.calculate_electrostatic_potential(test_args.relative_permittivity,
            test_args.distance, charge)
    with raises(TypeError):
        potential_law.calculate_electrostatic_potential(test_args.relative_permittivity,
            test_args.distance, 100)
