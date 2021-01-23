'''
You are given the starting_amount of candies. Whenver you eat a specific number of candies(eaten_candies), you get an
addtional candy.
What is the maximum number of candies you can eat? 
There was an efficient time implementation requirement, however, it is not possible to verify it at this point due to unavailability
of the particular environment.
For example, if starting_amount equals 3 and every time we eat 2 candies, we can eat 5 candies in total:
    - Eat 2. Get 1, Remaining 2.
    - Eat 2. Get 1, Remaining 1.
        - Eat 1.
'''
class Candies:
    @staticmethod
    def count_candies(starting_amount, eaten_candies):
        count = 0
        while starting_amount >= eaten_candies:
            count += eaten_candies
            starting_amount = starting_amount - eaten_candies + 1
        
        if starting_amount > 0:
            count += starting_amount

        return count

print(Candies.count_candies(3,2))
# please do not call the count_candies with (0,0); it will result in an infinite loop
