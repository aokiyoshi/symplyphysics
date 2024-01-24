from sympy import Eq, solve
from sympy.physics.units import speed_of_light

from symplyphysics import (Quantity, Symbol, print_expression, units, validate_input,
                           validate_output)


# Description
# The relativistic sum of velocities is the sum total of velocities in a body or system
# Law: v = (v1 + v2) / (1 + (v1 * v2) / c**2), where
# v1 is first velocity,
# v2 is second velocity,
# c is speed of light,
# v is relativistic sum of velocities.


# Conditions
# Non-zero rest mass
# Non-zero velocity

first_velocity = Symbol("first_velocity", units.velocity)
second_velocity = Symbol("second_velocity", units.velocity)
relativistic_sum_of_velocities = Symbol(
    "relativistic_sum_of_velocities", units.velocity)

law = Eq(
    relativistic_sum_of_velocities,
    (first_velocity + second_velocity) / (1 + (first_velocity * second_velocity) / speed_of_light**2))


def print_law() -> str:
    return print_expression(law)


@validate_input(
    first_velocity_=first_velocity,
    second_velocity_=second_velocity,
)
@validate_output(relativistic_sum_of_velocities)
def calculate_relativistic_sum_of_velocities(first_velocity_, second_velocity_):
    result_expr = solve(law, relativistic_sum_of_velocities)[0]
    velocity_applied = result_expr.subs({
        first_velocity: first_velocity_,
        second_velocity: second_velocity_,
    })
    return Quantity(velocity_applied)
