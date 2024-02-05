from collections import namedtuple
from pytest import fixture, raises
from symplyphysics import (assert_approx, errors, units, Quantity, SI, convert_to)

from symplyphysics.laws.thermodynamics import pressure_of_ideal_gas_from_height_and_temperature as pressure_of_ideal_gas

## Source of numbers: https://tsput.ru/res/fizika/1/ZAD_MKT/z_mkt_18_02.htm


@fixture(name="test_args")
def test_args_fixture():
    initial_pressure = Quantity(1e5 * units.pascal)
    atomic_weight = Quantity(0.029 * units.kilogram / units.mole)
    final_height = Quantity(6000 * units.meter)
    initial_height = Quantity(1000 * units.meter)
    temperature = Quantity(293 * units.kelvin)
    Args = namedtuple("Args",
        ["initial_pressure", "atomic_weight", "final_height", "initial_height", "temperature"])
    return Args(initial_pressure=initial_pressure,
        atomic_weight=atomic_weight,
        final_height=final_height,
        initial_height=initial_height,
        temperature=temperature)


def test_basic_law(test_args):
    result = pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
        test_args.atomic_weight, test_args.initial_height, test_args.final_height,
        test_args.temperature)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.pressure)
    result_final_pressure = convert_to(result, units.pascal).evalf(4)
    # Calculations in this example are bit inaccurate. Increase tolerance.
    assert_approx(result_final_pressure, 5.6e4, tolerance=0.01)


def test_bad_pressure(test_args):
    bad_pressure = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        pressure_of_ideal_gas.calculate_final_pressure(bad_pressure, test_args.atomic_weight,
            test_args.final_height, test_args.initial_height, test_args.temperature)
    with raises(TypeError):
        pressure_of_ideal_gas.calculate_final_pressure(100, test_args.atomic_weight,
            test_args.final_height, test_args.initial_height, test_args.temperature)


def test_bad_atomic_weight(test_args):
    bad_atomic_weight = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            bad_atomic_weight, test_args.final_height, test_args.initial_height,
            test_args.temperature)
    with raises(TypeError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure, 100,
            test_args.final_height, test_args.initial_height, test_args.temperature)


def test_bad_height(test_args):
    bad_height = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            test_args.atomic_weight, bad_height, test_args.initial_height, test_args.temperature)
    with raises(TypeError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            test_args.atomic_weight, 100, test_args.initial_height, test_args.temperature)
    with raises(errors.UnitsError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            test_args.atomic_weight, test_args.final_height, bad_height, test_args.temperature)
    with raises(TypeError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            test_args.atomic_weight, test_args.final_height, 100, test_args.temperature)


def test_bad_temperature(test_args):
    bad_temperature = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            test_args.atomic_weight, test_args.final_height, test_args.initial_height,
            bad_temperature)
    with raises(TypeError):
        pressure_of_ideal_gas.calculate_final_pressure(test_args.initial_pressure,
            test_args.atomic_weight, test_args.final_height, test_args.initial_height, 100)
