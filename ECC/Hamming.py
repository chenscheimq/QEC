# Python program to demonstrate
# hamming code
import random


def vis_res(res):
    stack = ''
    for i, bit in enumerate('0'+res):
        if i % calcRedundantBits(m) == 0 and i != 0:
            print(stack)
            stack = bit
        else:
            stack += bit
    print(stack)
    print()

def calcRedundantBits(m):
    # Use the formula 2 ^ r >= m + r + 1
    # to calculate the no of redundant bits.
    # Iterate over 0 .. m and return the value
    # that satisfies the equation

    for i in range(m):
        if (2 ** i >= m + i + 1):
            return i


def posRedundantBits(data, r):
    # Redundancy bits are placed at the positions
    # which correspond to the power of 2.
    j = 0
    k = 1
    m = len(data)
    res = ''

    # If position is power of 2 then insert '0'
    # Else append the data
    for i in range(1, m + r + 1):
        if (i == 2 ** j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1

    # The result is reversed since positions are
    # counted backwards. (m + r+1 ... 1)
    return res[::-1]


def calcParityBits(arr, r):
    n = len(arr)

    # For finding rth parity bit, iterate over
    # 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(arr[-1 * j])
            # -1 * j is given since array is reversed

        # String Concatenation
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
    return arr


def detectError(arr, nr):
    n = len(arr)
    res = 0

    # Calculate parity bits again
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(arr[-1 * j])

        # Create a binary no by appending
        # parity bits together.

        res = res + val * (10 ** i)

    # Convert binary to decimal
    return int(str(res), 2)


def fix_error(arr, location):
    res = ''
    arr = arr[::-1]
    for i in range(len(arr)):
        if i == (location-1):
            corrected = int(arr[i]) ^ 1
            res += str(corrected)
        else:
            res += str(arr[i])
    return res[::-1]


def flip_random_bit(arr):
    rand_bit = random.randint(0, len(arr) - 1)
    bit_flip = int(arr[rand_bit]) ^ 1
    return arr[:rand_bit] + str(bit_flip) + arr[rand_bit+1:]

# Enter the data to be transmitted
data = '010000010000000000000000000000000000000000000000000000000'
print("Data is: \n" + data)
# Calculate the no of Redundant Bits Required
m = len(data)
r = calcRedundantBits(m)
# Determine the positions of Redundant Bits
arr = posRedundantBits(data, r)
print("Data with redundant bits is \n" + arr)
# vis_res(arr[::-1])


# Determine the parity bits
arr = calcParityBits(arr, r)

# Data to be transferred
print("Data transferred is \n" + arr)
# vis_res(arr[::-1])
print(len(arr))

# Stimulate error in transmission by changing
# a bit value.
arr = flip_random_bit(arr)
print("Error Data is \n" + arr)
# vis_res(arr[::-1])

correction = detectError(arr, r)

if (correction == 0):
    print("There is no error in the received message.")
else:
    print("Correction is in location " + str(correction))

fixed_arr = fix_error(arr, correction)
print("Fixed Data is \n" + fixed_arr)
# vis_res(fixed_arr[::-1])

correction = detectError(fixed_arr, r)
if (correction == 0):
    print("There is no error in the received message.")
else:
    print("Correction is in location " + str(correction))