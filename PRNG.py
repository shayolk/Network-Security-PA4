from random import randint, getrandbits
from statsmodels.sandbox.stats.runs import runstest_1samp
import numpy as np
import math
from math import gcd


def linearCongruentialMethod(Xo, m, a, c, noOfRandomNums):
 
    randomNums = [0] * (noOfRandomNums)
    # Initialize the seed state
    randomNums[0] = Xo
 
    # Traverse to generate required
    # numbers of random numbers
    for i in range(1, noOfRandomNums):
         
        # Follow the linear congruential method
        randomNums[i] = ((randomNums[i - 1] * a) +
                                         c) % m
    
    return randomNums

def isPrime(number):
    if number == 1 or number == 2 or number == 3:
        return True
    if number == 4:
        return False

    index = 3
    while number > index:
        if number % index == 0:
            return False
        else:
            index += 1

    if(index == number):
        return True

def isCongruentNumber(number):
    # a - b = k * n
    # b = 3
    # k = 4
    # number - 3 = 4 * n
    if((number - 3) % 4 == 0):
        return True
    else:
        return False

def coprime(a, b):
    return gcd(a, b) == 1

class BBS:
    p = 0
    q = 0
    n = 0
    seed = 0
    generatedValues = []

    def __init__(self, p, q):
        self.p=0
        self.q=0
        self.n = 0
        self.seed = 0
        self.generatedValues = []

        self.setP(p)
        self.setQ(q)
        if(self.p > 0 and self.q > 0):
            self.__setN()
            self.__setSeed()

    def setP(self, p):
        if(not self.__checkParams(p)):
            self.p = p

    def setQ(self, q):
        if(not self.__checkParams(q)):
            self.q = q

    def __checkParams(self, number):
        isError = False
        if(not isPrime(number)):
            print(number, 'is not prime')
            isError = True

        return isError

    def __setN(self):
        self.n = self.p * self.q

    def __setSeed(self):
        while(not coprime(self.n, self.seed) and self.seed < 1):
            self.seed = randint(0, self.n - 1)

    def __generateValue(self):
        if(self.p > 0 and self.q > 0):
            x = 0
            while (not coprime(self.n, x)):
                x = randint(0, self.n)
            return pow(x, 2) % self.n

    def generateBits(self, amount):
        if(self.p == self.q):
            print('p should be diffrent than q')
            return False

        if (self.n == 0):
            print('N is equal 0')
            return False

        else:
            bitsArray = []
            amount += 1

            for i in range(1,amount):
                generatedValue = self.__generateValue()
                self.generatedValues.append(generatedValue)

                if(generatedValue % 2 == 0):
                    bitsArray.append(0)
                else:
                    bitsArray.append(1)

            return bitsArray

def RunsTest(seq):
	C = False
	if len(seq) >= 50:
		C = True
	stats = runstest_1samp(seq, correction = C)
	return {'z-score': stats[0], 'p-score': stats[1]}

def KSTest(seq, div):
        seq.sort()
        seq = [x / div for x in seq]
        N = len(seq)
        D_plus, D_minus = -10000000000000000, -10000000000000000

        for i in range(1, N + 1):
            x = i / N - seq[i-1]
            D_plus = max(D_plus, x)

        for i in range(1, N + 1):
            y = (i - 1) / N
            y = seq[i - 1] - y
            D_minus = max(D_minus, y)

        ans = max(math.sqrt(N) * D_plus, math.sqrt(N) * D_minus)
        return ans


if __name__ == '__main__':
    seed = int(input("Seed value for Linear Congruential Methdod: "))
    m = int(input("Modulus parameter for Linear Congruential Methdod: "))
    a = int(input("Multiplier term for Linear Congruential Methdod: "))
    c = int(input("Increment term for Linear Congruential Methdod: "))
    p = int(input("p for Blum Blum Shub Methdod: "))
    q = int(input("q for Blum Blum Shub Methdod: "))
    n = int(input("Length of random number sequence: "))


    sequence1 = linearCongruentialMethod(seed,m,a,c,n)

    obj = BBS(p,q)
    obj.generateBits(n)
    sequence2 = obj.generatedValues

    print("\n")
    print('Linear Congruential PRNG: ', sequence1)
    print("-----------------")
    print("Runs Test:")
    print(RunsTest(sequence1))
    print()
    print("Kolmogorov-Smirnov Test: ")
    print('D: ', KSTest(sequence1, m), '}')
    print()

    print('BlumBlumShub PRNG: ', sequence2)
    print("------------------")
    print("Runs Test:")
    print(RunsTest(sequence2))
    print()
    print("Kolmogorov-Smirnov Test: ")
    print('{D: ', KSTest(sequence2, obj.n ), '}')
    print()