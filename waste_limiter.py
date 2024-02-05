# just run this interactively to calculate things on-the-fly
# this module is to help avoid wasting inputs to a recipe
# Calculate exact iterations to do to have no waste for any input for any given module and lavish setting

from typing import List, Dict
from collections import Counter


# Each upgrade gives a different discount on materials
# Note that level '5' is the specialised upgrade and only counts for jobs with matching labour type
UPGRADE_DISCOUNTS: Dict[int, float] = {0: 0, 1: 0.1, 2: 0.25, 3: 0.40, 4: 0.45, 5: 0.50}


# If you took the lavish workspace discount this is its effect size - not it multiplicative, not additive
LAVISH_DISCOUNT = 0.05


def get_prime_factors(number: int) -> List[int]:
    divisor = 2
    prime_factors = []
    # just keep dividing by numbers
    while number > 1:
        while number % divisor == 0:
            prime_factors.append(divisor)
            number /= divisor
        divisor += 1 + (divisor & 0x1)
    return prime_factors


def lowest_common_multiple(*numbers: int) -> int:
    # get the prime factors of each number - this will be what we work with
    numbers_prime_factors = [get_prime_factors(number) for number in numbers]
    # find out the maximum number of times a given prime appears across all input numbers
    max_prime_factors = {}
    for number_prime_factors in numbers_prime_factors:
        for prime, count in Counter(number_prime_factors).items():
            if prime not in max_prime_factors or max_prime_factors[prime] < count:
                max_prime_factors[prime] = count
    # multiply out each prime by the maximum number of times it appeared
    # taking the maximum 'cancels out' common prime factors - what remains is what is required to hit lowest common multiple
    result = 1
    for prime, count in max_prime_factors.items():
        result *= prime**count
    return result


def calculate_loss(
    iterations: int, input_per: float, upgrade_lvl: int, has_lavish: bool
):
    consumption_rate = 1
    consumption_rate *= UPGRADE_DISCOUNTS[upgrade_lvl]
    if has_lavish:
        consumption_rate *= 1 - LAVISH_DISCOUNT
    total_inputs = iterations * input_per * consumption_rate
    loss = total_inputs - int(total_inputs)
    return loss


def find_best(input_per, upgrade_lvl, has_lavish):
    best_loss = 1e6
    best_iteration = 0
    for i in range(1, 10000):
        this_loss = calculate_loss(i, input_per, upgrade_lvl, has_lavish)
        if this_loss < best_loss:
            iteration_gap = i - best_iteration
            best_iteration = i
            best_loss = this_loss
            # print(f"Better at {i}, after {iteration_gap} iterations : {this_loss:.2f}")
    return best_iteration, best_loss


def find_best_all(inputs_per: List[int], upgrade_lvl: int, has_lavish: bool):
    best_iterations = [
        find_best(input_per, upgrade_lvl, has_lavish)[0] for input_per in inputs_per
    ]
    this_lcm = 1
    for best_iteration in best_iterations:
        this_lcm = lowest_common_multiple(this_lcm, best_iteration)
    print(f"Got LCM across materials of {this_lcm}")
    return this_lcm


### And this is how I used it when playing...

# quicklime, lvl4, lavish :: 400
find_best(1, 4, True)

# iron concentrate
find_best(3, 5, True)

# iron bar, lvl5, lavish :: 40
find_best(1, 5, True)

# gold
find_best(1, 5, True)

# steel :: 20
find_best(2, 5, True)

# cement, lvl5, lavish
find_best(1, 5, True)  # 40

find_best_all([1, 2.5], 5, True)


# steel :: 20
find_best(2, 5, True)

# rebar :: 20
find_best(2, 5, True)

# rivet :: 40
find_best(1, 5, True)

# cement
find_best_all([1, 2.5], 3, True)

# concrete :: 50
find_best_all([1, 2, 5], 3, True)

# pipe :: 40
find_best(1, 5, True)

# plastic :: 5
find_best(4, 1, False)
