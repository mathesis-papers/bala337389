import argparse
from fractions import Fraction
from math import comb, factorial
import json
from functools import lru_cache


def multiply(first, second, degree):
    return [sum((first[index] * second[power - index]
                 for index in range(power + 1)), Fraction(0))
            for power in range(degree + 1)]


def inverse(series, degree):
    result = [Fraction(1, 1) / series[0]]
    for power in range(1, degree + 1):
        result.append(-sum(series[index] * result[power - index]
                           for index in range(1, power + 1)) / series[0])
    return result


def square_root(series, degree):
    assert series[0] == 1
    result = [Fraction(1)]
    for power in range(1, degree + 1):
        result.append((series[power] - sum(result[index] * result[power - index]
                                          for index in range(1, power))) / 2)
    return result


def binomial_value(degree, parameter, odd=False):
    return sum(Fraction(comb(2 * degree + int(odd), 2 * index) * comb(2 * index, index))
               * parameter ** (degree - index) for index in range(degree + 1))


@lru_cache(maxsize=8192)
def integer_value(degree, parameter):
    return sum(comb(2 * degree, 2 * index) * comb(2 * index, index)
               * parameter ** (degree - index) for index in range(degree + 1))


def column_sum(degree, parameter):
    if degree == 0:
        return 1
    result = 0
    if parameter in (1, 2):
        step = 3 if parameter == 1 else 2
        for first in range(degree // step + 1):
            limit = degree - step * first
            for second in range(limit + 1):
                result += (comb(degree, first)
                           * comb(degree if parameter == 1 else 2 * degree, second)
                           * comb(3 * degree - step * first - second - 1,
                                  limit - second))
        return result
    for first in range(degree + 1):
        for second in range(min(first, degree - first) + 1):
            for third in range(degree - first - second + 1):
                result += (comb(degree, first) * comb(first, second)
                           * comb(2 * degree, third)
                           * comb(3 * degree - first - second - third - 1,
                                  degree - first - second - third))
    return result


def generalized_binomial(parameter, degree):
    value = Fraction(1)
    for index in range(degree):
        value *= Fraction(parameter - index, index + 1)
    return value


def sibling_checks():
    counts = {'odd_recurrence_comparisons': 0, 'square_identity_comparisons': 0,
              'column_sum_comparisons': 0, 'gauss_comparisons': 0,
              'supercongruence_comparisons': 0, 'kummer_identity_comparisons': 0}
    for degree in range(25):
        for parameter in range(-12, 37):
            left = sum((-1) ** index * generalized_binomial(parameter, index)
                       * generalized_binomial(2 * degree - parameter, degree - index)
                       for index in range(degree + 1))
            right = ((-1) ** degree * 4 ** degree
                     * generalized_binomial(Fraction(parameter - 1, 2), degree))
            assert left == right, (degree, parameter)
            counts['kummer_identity_comparisons'] += 1
    for parameter in range(-8, 17):
        for degree in range(25):
            value = integer_value(degree, parameter)
            squared = sum((parameter - 4) ** (2 * degree - index)
                          * comb(2 * index, index) ** 2
                          * comb(2 * degree + index, 2 * index)
                          for index in range(2 * degree + 1))
            assert squared == value ** 2, (degree, parameter)
            counts['square_identity_comparisons'] += 1
            if degree >= 2:
                left = degree * (2 * degree + 1) * (4 * degree - 3)
                left *= binomial_value(degree, Fraction(parameter), odd=True)
                middle = (4 * degree - 1) * (4 * (parameter + 4) * degree ** 2
                          - 2 * (parameter + 4) * degree - parameter - 2)
                middle *= binomial_value(degree - 1, Fraction(parameter), odd=True)
                last = ((parameter - 4) ** 2 * (degree - 1)
                        * (2 * degree - 1) * (4 * degree + 1))
                last *= binomial_value(degree - 2, Fraction(parameter), odd=True)
                assert left == middle - last, (degree, parameter)
                counts['odd_recurrence_comparisons'] += 1
    for parameter in (1, 2, 3):
        for degree in range(17):
            assert column_sum(degree, parameter) == integer_value(degree, parameter)
            counts['column_sum_comparisons'] += 1
    for parameter in range(-2, 9):
        for prime in (2, 3, 5, 7):
            for level in range(1, 4):
                for multiplier in range(1, 4):
                    degree = multiplier * prime ** level
                    difference = (integer_value(degree, parameter)
                                  - integer_value(degree // prime, parameter))
                    assert difference % (prime ** level) == 0
                    counts['gauss_comparisons'] += 1
    for parameter in (1, 2, 3):
        primes = (3, 5, 7, 11) if parameter == 2 else (5, 7, 11)
        for prime in primes:
            for level in (1, 2):
                for multiplier in range(1, 4):
                    degree = multiplier * prime ** level
                    difference = (integer_value(degree, parameter)
                                  - integer_value(degree // prime, parameter))
                    assert difference % (prime ** (2 * level)) == 0
                    counts['supercongruence_comparisons'] += 1
    return {'status': 'PASS', 'arithmetic': 'exact integer and rational',
            'kummer_identity': {'degrees': [0, 24], 'parameters': [-12, 36]},
            'square_and_odd_recurrence': {'degrees': [0, 24], 'parameters': [-8, 16]},
            'column_sums': {'degrees': [0, 16], 'parameters': [1, 2, 3]},
            'gauss': {'parameters': [-2, 8], 'primes': [2, 3, 5, 7],
                      'levels': [1, 3], 'multipliers': [1, 3]},
            'supercongruences': {'parameters': [1, 2, 3], 'levels': [1, 2],
                                'multipliers': [1, 3],
                                'primes_k2': [3, 5, 7, 11],
                                'primes_k1_k3': [5, 7, 11]},
            'checks': counts,
            'scope': 'Finite comparisons; asymptotic statements have written proofs in note.tex.'}


def check(degree):
    parameters = [Fraction(value) for value in range(17)]
    parameters += [Fraction(-7), Fraction(-4), Fraction(-1), Fraction(1, 4), Fraction(7, 3)]
    counts = {'coefficient_comparisons': 0, 'recurrence_comparisons': 0,
              'factorial_transform_comparisons': 0, 'initial_array_entries': 0}
    for parameter in parameters:
        discriminant = [Fraction(1), -2 * (parameter + 4), (parameter - 4) ** 2]
        discriminant += [Fraction(0)] * (degree - 2)
        inner = square_root(discriminant, degree)
        numerator = inner.copy()
        numerator[0] += 1
        numerator[1] += parameter - 4
        radical = square_root([entry / 2 for entry in multiply(
            numerator, inverse(discriminant, degree), degree)], degree)
        odd_denominator = multiply(discriminant, numerator, degree)
        odd_radical = square_root([2 * entry for entry in inverse(
            odd_denominator, degree)], degree)
        inverse_square = [Fraction(index + 1) for index in range(degree + 1)]
        first = [Fraction(1), parameter - 2, Fraction(1)] + [Fraction(0)] * (degree - 2)
        second = [Fraction(1), Fraction(2), Fraction(1)] + [Fraction(0)] * (degree - 2)
        phi = multiply(multiply(first, second, degree), inverse_square, degree)
        powers = [Fraction(1)] + [Fraction(0)] * degree
        values = []
        for power in range(degree + 1):
            value = binomial_value(power, parameter)
            assert value == radical[power] == powers[power], (parameter, power)
            assert binomial_value(power, parameter, odd=True) == odd_radical[power]
            assert binomial_value(power, Fraction(0)) == comb(2 * power, power)
            assert binomial_value(power, Fraction(4)) == comb(4 * power, 2 * power)
            values.append(value)
            counts['coefficient_comparisons'] += 5
            if power >= 2:
                left = power * (2 * power - 1) * (4 * power - 5) * value
                middle = (4 * power - 3) * (4 * (parameter + 4) * power ** 2
                           - 6 * (parameter + 4) * power + parameter + 6) * values[-2]
                last = (parameter - 4) ** 2 * (power - 1) * (2 * power - 3) * (4 * power - 1) * values[-3]
                assert left == middle - last, (parameter, power)
                counts['recurrence_comparisons'] += 1
            powers = multiply(powers, phi, degree)
    for power in range(61):
        for index in range(power + 1):
            rising = Fraction(1)
            for offset in range(power - index):
                rising *= Fraction(2 * index + 1, 2) + offset
            left = comb(power, index) * 4 ** (power - index) * rising / factorial(power - index)
            right = Fraction(factorial(2 * power), factorial(2 * index) * factorial(power - index) ** 2)
            assert left == right
            counts['factorial_transform_comparisons'] += 1
    expected = [1, 1, 2, 1, 3, 6, 1, 4, 19, 20, 1, 5, 34, 141, 70, 1, 6, 51, 328, 1107, 252]
    actual = [binomial_value(row, Fraction(diagonal - row))
              for diagonal in range(6) for row in range(diagonal + 1)]
    assert actual == expected
    counts['initial_array_entries'] = len(expected)
    return {'status': 'PASS', 'arithmetic': 'exact rational; no floating-point operations',
            'degree_range': [0, degree], 'parameters': [str(value) for value in parameters],
            'factorial_transform_degree_range': [0, 60], 'checks': counts,
            'scope': 'Finite coefficient, radical, recurrence and boundary comparisons; unbounded statements have written proofs in note.tex.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--degree', type=int, default=24)
    parser.add_argument('--siblings', action='store_true')
    arguments = parser.parse_args()
    if not 2 <= arguments.degree <= 60:
        parser.error('--degree must be between 2 and 60')
    print(json.dumps(sibling_checks() if arguments.siblings else check(arguments.degree), indent=2))
