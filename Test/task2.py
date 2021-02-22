'''
There are N coins, each showing either heads or tails. We would like all the coins to form a sequence of alternating
heads and tails. What is the minimum number of coins that must be reversed to achieve this?

Write a function:
    
    def solution(A)

that, given an array A consisting of N integers representing the coins, returns the minimum number of coins that must be
reversed. Consecutive elements of array A represent consecutive coins and contain either a 0(heads) or a 1(tails).

Examples:

1. Given array A = [1,0,1,0,1,1], the function should return 1. After reversing the sixth coin, we achieve an
alternating sequence of coins [1,0,1,0,1,0].

2. Given array A = [1,1,0,1,1], the function should return 2. After reversing first and fifth coins, we achieve an
alternating sequence [0,1,0,1,0].

3. Given array A = [0,1,0], the function should return 0. The sequence of coins is already alternating.

4. Given array A = [0,1,1,0], the function should return 2. We can reverse the first and second coins to get the
sequence: [1,0,1,0].

Assume that:
    
    - N is an integer within the range [1..100]
    - each element of array A is an integer that can have one of the following values: 0,1.

In your solution, focus on correctness. The performance of your solution will not be the focus of the assessment.
'''

def solution(A):
    # write your code in Python 3.6
    if len(A) < 2:
        print('A needs at least two elements.')
        return

    if len(A) == 2:
        if A[0] == A[1]:
            return 1
        else:
            return 0

    count = 0
    for num in range(len(A)-2):
        #print(A[num],A[num+1],A[num+2])
        if  (A[num] < A[num + 1]) and (A[num + 1] > A[num + 2]):
            continue
        if (A[num] > A[num + 1]) and (A[num + 1] < A[num + 2]):
            continue
        count += 1
    return count

A1 = [1,0,1,0,1,1]
A2 = [1,1,0,1,1]
A3 = [0,1]
A4 = [1,0,0,1]
A5 = [0,1,1,0]
A6 = [1,0]
A7 = [1,1]
A8 = [0,0]
A9 = [1,1,0]
A10 = [1,0,0]
A11 = [1]
A12 = [1,1]

print(solution(A12))

# below print syntax doesn't work with python 3.6
#print(f"A1 is {solution(A1)}")
#print(f"A2 is {solution(A2)}")
#print(f"A3 is {solution(A3)}")
#print(f"A4 is {solution(A4)}")
#print(f"A5 ia {solution(A5)}")
#print(f"A6 is {solution(A6)}")
#print(f"A7 is {solution(A7)}")
#print(f"A8 is {solution(A8)}")
#print(f"A9 is {solution(A9)}")
#print(f"A10 is {solution(A10)}")


