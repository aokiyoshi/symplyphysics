from collections import namedtuple
from pytest import approx, fixture, raises
from sympy import pi
from symplyphysics import (units, SI, convert_to, Quantity, errors, prefixes)
from symplyphysics.laws.electricity import magnetic_induction_of_linear_conductor_of_finite_length as induction_law

# Description
## Let the current in the conductor be 1 ampere, the distance from the conductor is 2 meter and the
## magnetic permeability of the medium is 10. Then, at the first angle of 45 degree (pi / 4 radian)
## and the second angle of 60 degree (pi / 3 radian), the magnetic induction will be equal to 603 nanotesla.
## https://www.indigomath.ru//raschety/EFaosd.html


@fixture(name="test_args")
def test_args_fixture():
    relative_permeability = 10
    current = Quantity(1 * units.ampere)
    first_angle = pi / 4
    second_angle = pi / 3
    distance = Quantity(2 * units.meter)

    Args = namedtuple("Args",
        ["relative_permeability", "current", "first_angle", "second_angle", "distance"])
    return Args(relative_permeability=relative_permeability,
        current=current,
        first_angle=first_angle,
        second_angle=second_angle,
        distance=distance)


def test_basic_induction(test_args):
    result = induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
        test_args.first_angle, test_args.second_angle, test_args.distance)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.magnetic_density)
    result = convert_to(result, prefixes.nano * units.tesla).evalf(5)
    assert result == approx(603, rel=0.01)


def test_swap_angle(test_args):
    result = induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
        test_args.second_angle, test_args.first_angle, test_args.distance)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.magnetic_density)
    result = convert_to(result, prefixes.nano * units.tesla).evalf(5)
    assert result == approx(603, rel=0.01)


def test_bad_relative_permeability(test_args):
    relative_permeability = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        induction_law.calculate_induction(relative_permeability, test_args.current,
            test_args.first_angle, test_args.second_angle, test_args.distance)


def test_bad_current(test_args):
    current = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        induction_law.calculate_induction(test_args.relative_permeability, current,
            test_args.first_angle, test_args.second_angle, test_args.distance)
    with raises(TypeError):
        induction_law.calculate_induction(test_args.relative_permeability, 100,
            test_args.first_angle, test_args.second_angle, test_args.distance)


def test_bad_angle(test_args):
    first_angle = Quantity(1 * units.coulomb)
    second_angle = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
            first_angle, test_args.second_angle, test_args.distance)
    with raises(AttributeError):
        induction_law.calculate_induction(test_args.relative_permeability, test_args.current, True,
            test_args.second_angle, test_args.distance)
    with raises(errors.UnitsError):
        induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
            test_args.first_angle, second_angle, test_args.distance)
    with raises(AttributeError):
        induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
            test_args.first_angle, True, test_args.distance)


def test_bad_distance(test_args):
    distance = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
            test_args.first_angle, test_args.second_angle, distance)
    with raises(TypeError):
        induction_law.calculate_induction(test_args.relative_permeability, test_args.current,
            test_args.first_angle, test_args.second_angle, 100)
