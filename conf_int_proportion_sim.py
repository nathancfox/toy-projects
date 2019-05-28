#!/usr/bin/python3
"""
Program: 95% Confidence Interval of a Proportion Simulation
Author: Nathan Fox <nchristopherfox@gmail.com>
Date Created: 2019-05-28
Date Modified: 2019-05-28

This program conducts a simulation to confirm the modified Wald's method
for calculating a 95% Confidence Interval (CI) for a proportion. It takes a
population proportion parameter, then draws s trials for n simulations
and reports the percentage of simulations where the calculated CI contained
the population proportion parameter.

Modified Wald's Method for 95% CI for a Proportion was taken from pg 39 of
Intuitive Biostatistics by Harvey Motulsky, ISBN-13 978-0-19-064356-0
"""

import argparse
import numpy as np

def mod_wald(successes, trials):
    """Calculate Modified Wald's Method 95% Confidence Interval for Proportion.

    Calculates a 95% confidence interval sourced from Intuitive Biostatistics,
    see note in script docstring. This method assumes several things:

    1) The sample was taken from the same distribution as the population.
       i.e. This sample is representative.
    2) All observations are independently drawn.
    3) All observations are reported accurately.

    Args:
        successes: integer; number of trials that gave the desired outcome
        trials: integer; total number of trials

    Returns:
        A tuple with 2 elements. tuple[0] is the lower bound of the confidence
        interval. tuple[1] is the upper bound.
    """
    p_hat = (successes + 2) / (trials + 4)
    w = 2 * np.sqrt((p_hat * (1-p_hat)) / (trials + 4))
    return (p_hat-w, p_hat+w)

def simulate(x, n, sample_size):
    """Simulate calculation of 95% CI for proportions from binomial data.

    Simulates n experiments, drawing sample_size data points from a distribution
    with a favorable proportion of x. Calculates a confidence interval for
    each, then displays the number of confidence intervals that actually
    contained the population parameter.

    Args:
        x: float; population proportion for favorable outcome
        n: integer; number of simulations
        sample_size: integer; number of trials per simulation

    Returns:
        Numpy array of size(n, 3). Each row is a simulation.
        Column 0: Lower bound of CI
        Column 1: Upper bound of CI
        Column 3: Float form of boolean(CI contains population parameter)
    """

    results = np.zeros((n, 3))
    for i in range(n):
        s = np.random.uniform(size=sample_size)
        s = s < x
        results[i] = (mod_wald(successes=s.sum(), trials=sample_size) + (-1.0,))
        results[i, 2] = float((results[i, 0] <= x) and (results[i, 1] >= x))
    return results

def main():
    """Simulation to verify 95% Confidence Interval for Proportion.

    Prints n, number of simulations where the CI actually contained the
    population parameter, and the percentage version of the last value. To see
    command line arguments, run 'python conf_int_proportion_sim.py -h'.
    """
    parser = argparse.ArgumentParser(description=('Confirms 95% Confidence '
                                        'Interval by simulation. Sample size '
                                        'of 40 per simulation. Takes 1 '
                                        'parameter:\n\tP: Population '
                                        'percentage of favorable outcomes'))
    parser.add_argument('P', type=float,
                        help='Proportion of population with favorable outcome')
    parser.add_argument('-n', default=100, type=int,
                        help='Number of simulations to be run')
    parser.add_argument('-s', default=40, type=int,
                        help=('Number of trials in each simulation '
                              '(sample size)'))

    args=parser.parse_args()
    results = simulate(x=args.P, n=args.n, sample_size=args.s)
    print('\nResults\n====================\n')
    # print(results)
    print('# of Simulations:           {}'.format(args.n))
    print('# of CIs Including True P:  {}'.format(int(results[:,2].sum())))
    print('% of Sims Including True P: {}'.format(results[:,2].sum()/args.n))
    print()

if __name__=='__main__':
    main()
