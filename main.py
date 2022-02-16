import time

import matplotlib.pyplot as plt
import numpy as np
import mplcursors
from numba import jit
import matplotlib as mpl
mpl.use('tkAgg')

# globals
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DAYS_PER_MONTH[:] = map(lambda ele: ele + 1, DAYS_PER_MONTH)


# a function to get number counts
@jit
def set_number_counts(number: int, count_array: np.ndarray):
    # find the tens, hundreds etc.
    while number > 0:
        number, leftover = divmod(number, 10)
        count_array[leftover] += 1


@jit
def set_number(day: int, month: int, year: int, hist_array: np.ndarray, result_array: np.ndarray, counter: int):
    # reset the hist arrays
    hist_array[:] = 0

    # make the histogram
    set_number_counts(year, hist_array)
    set_number_counts(month, hist_array)
    set_number_counts(day, hist_array)

    # get the maximum
    index = np.argmax(hist_array)

    # save the maximum
    result_array[counter, 0] = index
    result_array[counter, 1] = hist_array[index]
    result_array[counter, 2] = year
    result_array[counter, 3] = month
    result_array[counter, 4] = day
    result_array[counter, 5] = counter

    return counter + 1


def get_repetition_hist(end_year: int):
    # check the year
    assert end_year < 2**16 - 1

    # create variables:
    hist_array = np.zeros((10,), dtype='uint8')

    # calculate the amount of days and make an array to save the counter, the highest number, frequency of this number
    # and date
    number_days = end_year * 365 + end_year // 4
    maximum_over_time = np.zeros((number_days, 1 + 2 + 3), dtype='uint32')

    # iterate over all dates and count occurrences
    counter = 0
    for year in range(1, end_year + 1):

        # go over the months
        for month in range(1, 13):

            # get the amount of days
            days_per_month = DAYS_PER_MONTH[month - 1]
            if month == 2 and year % 4 == 0:
                days_per_month += 1

            # go over all the days
            for day in range(1, days_per_month):
                counter = set_number(day, month, year, hist_array, maximum_over_time, counter)
    return maximum_over_time


if __name__ == '__main__':
    a = time.time()
    res = get_repetition_hist(3000)
    print(f'Elsapsed time: {time.time() - a}')
    # target_bools = res[:, 1] > 2
    target_bools = res[:, 1] > 0
    plt.plot(res[target_bools, 5], res[target_bools, 1], 'x')
    mplcursors.cursor().connect("add", lambda sel: sel.annotation.set_text(f'{res[int(sel.target[0]), 4]}.{res[int(sel.target[0]), 3]}.{res[int(sel.target[0]), 2]} - {res[int(sel.target[0]), 1]}x [{res[int(sel.target[0]), 0]}] - {sel.target[0]}'))
    plt.show()
