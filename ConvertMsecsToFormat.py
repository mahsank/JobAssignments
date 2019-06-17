#!/usr/bin/env python3

def convert_milliseconds_to_format(milliseconds):
    """ TODO
    Convert a given milliseconds to a list of integers of the form
    [days, hours, minutes, seconds, milliseconds]
    Assume that:
    1 day = 24 hours,
    1 hour = 60 minutes,
    1 minute = 60 seconds
    1 second = 1000 milliseconds
    Params:
    - milliseconds: the milliseconds (integer) to convert
    Return value:
    - a list of 5 integers: (days, hours, minutes, seconds, milliseconds)
    Exceptions:
    - Raise ConversionError on any possible errors with a meaningful message
    #return [0, 0, 0, 0, 0]
    "As a job assignment, I was asked to implement the function below."
    "The program is slightly modified to make it work as a general-purpose
    function"
    """
    try:
        if not isinstance(milliseconds, int):
            raise TypeError
        elif abs(milliseconds) > 2 ** 31 - 1:
            raise ValueError
        elif milliseconds < 0:
            raise ValueError
    except ValueError:
        print("Incorrect value supplied for milliseconds.")
    except TypeError:
        print("Milliseconds need to be a positive integer value.")
    else:
        result = []
        # time = [day, hour, minute, second]
        time_in_seconds = [24*3600, 3600, 60, 1]
        time_in_milliseconds = [i*1000 for i in time_in_seconds]
        for t in time_in_milliseconds:
            temp,milliseconds = divmod(milliseconds, t)
            result.append(temp)
        result.append(milliseconds)
        return result

# Test valid conversion with static test data
test_data = {
    0: [0, 0, 0, 0, 0],
    60: [0, 0, 0, 0, 60],
    1000: [0, 0, 0, 1, 0],
    10: [0, 0, 0, 0, 10],
    94456372: [1, 2, 14, 16, 372],
    256148480: [2, 23, 9, 8, 480],
    335319745: [3, 21, 8, 39, 745],
    402061620: [4, 15, 41, 1, 620],
    436869759: [5, 1, 21, 9, 759],
    512348349: [5, 22, 19, 8, 349],
    36471736: [0, 10, 7, 51, 736],
    65491123: [0, 18, 11, 31, 123],
    217131201: [2, 12, 18, 51, 201],
    501919788: [5, 19, 25, 19, 788]
    }

for i in test_data.keys():
    calculated_data = convert_milliseconds_to_format(i)
    if test_data[i] == calculated_data:
        print("Conversion of " + str(i) + " is successful." )
        print("Actual Data: ",test_data[i])
        print("Calculated Data: ", calculated_data)
        print()
    else:
        print("Calculated data does not match with the actual data.")
        print("Something is wrong with the function logic.")

#TODO
# Implement the logic for testing invalid conversions which should trigger
# errors
