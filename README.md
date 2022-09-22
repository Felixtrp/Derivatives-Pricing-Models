# Derivatives-Pricing-Models
This repo contains programmes exploring different methods for determining the prices of derivatives.

The repo contains programs that use a number of different implementations.

## Analytic Methods
The Black-Scholes equation can be used to determine the value of certain derivatives (European calls and pits) and has an analytic solution.
The equation relies on a number of simplifying assumptions.  The equation - and modified versions of the equation - are still widely used as basis for many option pricing models.
The programs in this repo explore the equation, and find solutions to it using a number of different numerical methods.

## Binomial Methods
Binomial methods are an example of a numerical method for calculating options prices.  The stock price is modelled as a series of Bernoulli trials, occurring over a set number of time steps between the current time and expiry - the price can increase by a factor u, with a probability p, or decearse by a factor d, with probability (1-p).  A binomial tree is then drawn for all possible values the price can take between now and expiry.  p, u and d are chosen to ensure that the expected drift and volatility are the same as the stock price being modelled.

For European-style options, the value of the option at expiry for each possible outcome is easily foun, given the payoff function for the specific optino.  Then, the price at each point on the tree in the step immediately prior to expiry can be found: it is the expected value of the option {=pu + (1-p)d}, discounted by the appropriate interest rate, exp(r delta_t).  Iteratively working backwards through the tree, a value of the option at the current time is found.  This technique is easily applied to any European-option (exercise not before expiry), with any specified payoff function, as long as the initial stock price, interest rate, volatility and time-to-expiry are given.

For American options, the opportunity for early exercise is easily incorporated.  At a time-step m, if the option is exercised, the option will produce payoff(S_m).  If it is not exercised, the option will have the value of the discounted expected value for the subsequent timestep (just like the European option).  The value of the option will be tied to the optimal exercise of the option, and so will be the maximum of these two quantities.  Noting whether or not it is optimal to eercise an option will also generate the exercise boundary s_f(t), which exists for certain American options.

## Monte Carlo Methods - Stock Pricing
To model complex or 'exotic' options, it issometimes necessary to resort to Monte-Carlo methods: producing a simulation of how the value derived from a single derivative evolves over time due to random variation in the price of an underlying or any other factors), and then running this simulation a large number of times to obtain an expected value (and thus, fair price for the option at the current time.

These method are often computationally expenseive, and should be avoided when analytic or other more efficient numerical methods are available.  However, for the most complex types of derivatives, the Monte-Carlo method offers a 'last resort' method, when nothing else will suffice.

Before options are priced using this method, it is firt necessary to be able to accurately simulate the movement of underlyings.  It is typically assumed that stock prices evolve via geometric Brownian motion.  This program demonstrate simulations based on this assumption, and compares the results with the analytic soltion derived via Ito calculus  Results of this program are shown below.

![Stock Price Simulations](https://user-images.githubusercontent.com/64906690/191731131-1ffe4e40-ef8a-40b0-a493-20ffa8e0db0d.png)

![Stock Price Probability Distributions Experiment and Analytic](https://user-images.githubusercontent.com/64906690/191731185-f303733a-f269-4b1c-b83a-a5bc339b9382.png)

## Monte Carlo Methods - Options Pricing
In a Monte-Carlo program, the values of certain European options are calculated and compared with the analytic results as a test of the program.  Then, path-dependent options are investigated and their values evaluated.
