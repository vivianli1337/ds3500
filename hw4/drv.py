# import libraries
import copy
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns

class DRV:
    """ A model for discrete random variables and uniform and normal continous distributions where outcomes are numeric """
    def __init__(self, dist=None, type='discrete', min=None, max=None, mean=None, stdev=None, bins=None):
        if isinstance(dist, str):
            # Assuming the string is formatted as "value1: probability1\nvalue2: probability2\n..."
            self.dist = {float(val.split(':')[0].strip()): float(val.split(':')[1].strip()) for val in dist.split('\n') if val}
        # Handle dictionary input
        elif isinstance(dist, dict):
            self.dist = copy.deepcopy(dist)
        else:
            self.dist = {}
        
        # discrete variables
        if type == 'discrete':
            if dist is None:
                self.dist = {}
            else:
                self.dist = copy.deepcopy(dist)

        # normal distribution
        elif type == 'normal':
            # print alert when values not entered
            assert mean is not None and stdev is not None and bins is not None, "mean, stdev, and bin values are required for normal distribution"

            # normal distribution with discrete random variable
            # calculated using the normal probability density function 
            outcome = np.linspace(mean - 3 * stdev, mean + 3 * stdev, bins)
            prob = np.exp(-(outcome - mean)**2 / (2 * stdev**2)) / (stdev * np.sqrt(2 * np.pi))
            
            # normalize prob
            prob /= np.sum(prob)  
            self.dist = dict(zip(outcome, prob))

        # uniform distribution
        elif type == 'uniform':
            # print alert when values not entered
            assert min is not None and max is not None and bins is not None, "min, max, and bin values are required for uniform distribution"

            # uniform distribution with discrete random variable
            outcome = np.linspace(min, max, bins)
            prob = np.full_like(outcome, 1/bins)
            self.dist = dict(zip(outcome, prob))

        else:
            # print alert when invalid type input
            raise ValueError("Invalid distribution type inputted")
        
    

    def __getitem__(self, x):
        return self.dist.get(x, 0.0)

    def __setitem__(self, x, p):
        self.dist[x] = p

    def apply(self, other, op):
        """ Apply a binary operator to self and other """
        Z = DRV()
        items = self.dist.items()
        oitems = other.dist.items()
        for x, px in items:
            for y, py in oitems:
                Z[op(x, y)] += px * py
        return Z

    def applyscalar(self, a, op):
        Z = DRV()
        items = self.dist.items()
        for x, p in items:
            Z[op(x,a)] += p
        return Z

    def __add__(self, other):
        return self.apply(other, lambda x, y: x + y)

    def __radd__(self, a):
        return self.applyscalar(a, lambda x, c: c + x)

    def __rmul__(self, a):
        return self.applyscalar(a, lambda x, c: c * x)

    def __rsub__(self, a):
        return self.applyscalar(a, lambda x, c: c - x)

    def __sub__(self, other):
        return self.apply(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self.apply(other, lambda x, y: x * y)

    def __truediv__(self, other):
        # might require div by 0 handling
        return self.apply(other, lambda x, y: x / y)

    def __pow__(self, other):
        return self.apply(other, lambda x, y: x ** y)

    def __repr__(self):
        xp = sorted(self.dist.items())
        rslt = ''
        for x, p in xp:
            rslt += str(round(x)) + " : " + str(round(p, 8)) + "\n"
        return rslt
    
    def random(self, n=1000):
        """ generate a sequence of random numbers based on the distribution """
        outcome = list(self.dist.keys())
        prob = list(self.dist.values())

        # generate random samples
        samples = random.choices(outcome, weights=prob, k=n)
        return samples

    def plot(self, cumulative=False, log_scale=False, trials=0, bins=20):
        """ Plot graph w/ option to overlay cumulative distribution and/or log y scale """
        outcome = list(self.dist.keys())
        prob = list(self.dist.values())

        if trials == 0:
            plt.bar(outcome, prob, label='Probability Distribution')
        else:
            # generate random samples based on the distribution
            samples = self.random(n=trials)
            sns.histplot(samples, stat='probability', cumulative=cumulative, log_scale=log_scale, bins=bins,
                         discrete=True, label='Sample Distribution')

        if cumulative:
            c_prob = np.cumsum(prob)
            # overlay the cumulative distribution
            plt.plot(outcome, c_prob, color='red', label='Cumulative Distribution')

        if log_scale:
            plt.yscale('log')

        plt.title('N distribution')
        plt.xlabel('Value x')
        plt.ylabel('Probability p(x)')

        plt.legend()  

        plt.show()

    def ev(self):
        """ compute expected valye (E) """
        expected_val = 0.0
        for outcome, prob in self.dist.items():
            expected_val += outcome * prob
        return expected_val

    def stdev(self):
        """ compute standard deviation (stdev) """
        mean = self.ev()
        variance = 0.0
        for outcome, prob in self.dist.items():
            variance += (outcome - mean) ** 2 * prob
        std = np.sqrt(variance)
        return std
    





def main():

    X = DRV({1:0.60, 3:0.40})
    Y = DRV({0:0.20, 2:0.50, 5:0.30})

    Z = X + Y
    print(Z.dist)
    print(Z)
    Z.plot(cumulative=True, log_scale=False, trials=0, bins=20)

    W = 10 + Z
    W.plot(cumulative=True, log_scale=False, trials=0, bins=20)


if __name__ == '__main__':
    main()
