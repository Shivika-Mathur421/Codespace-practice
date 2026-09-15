# WAP to make a function that takes a list of numbers
# and gives the second largest number.

def second_largest(numbers):
    if len(numbers) < 2:
        return "List should contain at least two numbers"

    largest = numbers[0]
    second_largest_num = numbers[1]

    if largest < second_largest_num:
        largest, second_largest_num = second_largest_num, largest

    for num in numbers[2:]:
        if num > largest:
            second_largest_num = largest
            largest = num
        elif num > second_largest_num:
            second_largest_num = num

    return second_largest_num


# Example
print(second_largest([12, 35, 1, 10, 34]))
