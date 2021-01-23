'''
Write a function tuple_slice that takes a startIndex and endIndex and returns a slice startIndex:endIndex(exclusive);
the function should return the result as plain numbers
For example, for the following function call, tuple_slice should return
35,14,62
'''


def tuple_slice(startIndex, endIndex, tup):
    numbers = ""
    for i in range(startIndex,endIndex):
        if i == endIndex - 1:
            numbers = numbers + str(tup[i])
        else:
            numbers = numbers + str(tup[i]) + ","
    return numbers

if __name__ == "__main__":
    print(tuple_slice(1, 4, (76, 35, 14, 62, 12)))
