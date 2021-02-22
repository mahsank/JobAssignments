'''
You are given an implementation of a function solution that, given a positive integer N, prints to standard output,
another integer, which was formed by reversing a decimal representation of N. The leading zeros of the resulting
integers should not be printed by the function.

Examples:
1. Given N = 54321, the function should print 12345.
2. Given N = 10011, the function should print 11001.
3. Given N = 1, the function should print 1.

The attached code is still incorrect for some inputs, Despite the error(s), the code may produce a correct answer for
the example test cases. The goal of the exercise is to find and fix bugs(s) in the implementation. You can modify at
least three lines.

Assume that:
    - N is an integer with the reange [1,1,000,000,000].
'''

def solution(N):
    enable_print = N % 10
    #print(enable_print)
    while N > 0:
        if N % 10 != 0:
            enable_print = 1
        if enable_print == 1:
            print(N % 10, end="")
        N = N // 10
        #print(N)
    print()

solution(105)
solution(1005)
solution(54321)
solution(10011)
solution(100)
solution(99)
solution(100000000000000)
solution(54321111)
solution(111110)
solution(300001)

