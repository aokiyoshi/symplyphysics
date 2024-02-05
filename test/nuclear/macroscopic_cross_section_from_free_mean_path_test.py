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
from symplyphysics.laws.nuclear import macroscopic_cross_section_from_free_mean_path as macro_cs

# From https://www.nuclear-power.com/nuclear-power/reactor-physics/nuclear-engineering-fundamentals/neutron-nuclear-reactions/macroscopic-cross-section/


@fixture(name="test_args")
def test_args_fixture():
    # boron carbide mean free path
    mean_free_path = Quantity(0.01186 * units.centimeter)
    Args = namedtuple("Args", ["y"])
    return Args(y=mean_free_path)


def test_basic_cross_section(test_args):
    result = macro_cs.calculate_cross_section(test_args.y)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, 1 / units.length)
    result_cross_section = convert_to(result, 1 / units.centimeter).evalf(4)
    # boron carbide macroscopic cross-section is 84.3 cm^-1
    assert_approx(result_cross_section, 84.3)


def test_bad_microscopic_cross_section():
    yb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        macro_cs.calculate_cross_section(yb)
    with raises(TypeError):
        macro_cs.calculate_cross_section(100)
