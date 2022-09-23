# Derivatives-Pricing-Models
This repo contains programmes exploring different methods for determining the prices of derivatives.

The repo contains programs that use a number of different implementations.

## Analytic Methods
The Black-Scholes equation can be used to determine the value of certain derivatives (European calls and pits) and has an analytic solution.
The equation relies on a number of simplifying assumptions.  The equation - and modified versions of the equation - are still widely used as basis for many option pricing models.
The programs in this repo explore the equation, and find solutions to it using a number of different numerical methods.

## Geometric Brownian Motion - Stock Pricing
To model complex or 'exotic' options, it issometimes necessary to resort to Monte-Carlo methods: producing a simulation of how the value derived from a single derivative evolves over time due to random variation in the price of an underlying or any other factors), and then running this simulation a large number of times to obtain an expected value (and thus, fair price for the option at the current time.

These method are often computationally expenseive, and should be avoided when analytic or other more efficient numerical methods are available.  However, for the most complex types of derivatives, the Monte-Carlo method offers a 'last resort' method, when nothing else will suffice.

Before options are priced using this method, it is firt necessary to be able to accurately simulate the movement of underlyings.  It is typically assumed that stock prices evolve via geometric Brownian motion.  This program demonstrate simulations based on this assumption, and compares the results with the analytic soltion derived via Ito calculus  Results of this program are shown below.

![Stock Price Simulations](https://user-images.githubusercontent.com/64906690/191731131-1ffe4e40-ef8a-40b0-a493-20ffa8e0db0d.png)

![Stock Price Probability Distributions Experiment and Analytic](https://user-images.githubusercontent.com/64906690/191731185-f303733a-f269-4b1c-b83a-a5bc339b9382.png)


## Binomial Methods
Binomial methods are an example of a numerical method for calculating options prices.  The stock price is modelled as a series of Bernoulli trials, occurring over a set number of time steps between the current time and expiry - the price can increase by a factor u, with a probability p, or decearse by a factor d, with probability (1-p).  A binomial tree is then drawn for all possible values the price can take between now and expiry.  p, u and d are chosen to ensure that the expected drift and volatility are the same as the stock price being modelled.

The binomial tree demonstrates a clear similarity to the Monte-Carlo stock pricing plot.  The plot of the binomial tree - with weighted branches - was produced by a random walk through the possible paths.  Althogh there is no randomness in the binomial tree pricing model, the incorporation of a random walk provides insight into how the process replicates a system similar to geometric brownianmotion in the limit.

![BinomialStockPriceProbabilities](https://user-images.githubusercontent.com/64906690/192006212-f9f2717b-c892-4f28-b148-4563065fff0b.png)

The binomial tree demonstrates a clear similarity to the Monte-Carlo stock pricing plot.  The plot of the binomial tree - with weighted branches - was produced by a random walk through the possible paths.  Althogh there is no randomness in the binomial tree pricing model, the incorporation of a random walk provides insight into how the process replicates a system similar to geometric brownianmotion in the limit.

![BinomialStockPriceProbabilities](https://user-images.githubusercontent.com/64906690/192006212-f9f2717b-c892-4f28-b148-4563065fff0b.png)

For European-style options, the value of the option at expiry for each possible outcome is easily foun, given the payoff function for the specific optino.  Then, the price at each point on the tree in the step immediately prior to expiry can be found: it is the expected value of the option {=pu + (1-p)d}, discounted by the appropriate interest rate, exp(r delta_t).  Iteratively working backwards through the tree, a value of the option at the current time is found.  This technique is easily applied to any European-option (exercise not before expiry), with any specified payoff function, as long as the initial stock price, interest rate, volatility and time-to-expiry are given.

For American options, the opportunity for early exercise is easily incorporated.  At a time-step m, if the option is exercised, the option will produce payoff(S_m).  If it is not exercised, the option will have the value of the discounted expected value for the subsequent timestep (just like the European option).  The value of the option will be tied to the optimal exercise of the option, and so will be the maximum of these two quantities.  Noting whether or not it is optimal to exercise an option will also generate the exercise boundary s_f(t), which exists for certain American options.

The program is able to replicate both of these types of options, for a variety of payoff functions.  Different payoff functions correspond to different types of options: calls, puts, cash-or-nothing options etc.  The plot below shows the time evolutions of calls and puts at the same strike price for both American and European style exercise rights.

![BinomialOptionsPricingPic](https://user-images.githubusercontent.com/64906690/192006645-bf44d99c-97cf-48c4-80de-fed80206efc1.png)

For calls, American and European options have identical value (so long as there are no dividends).  It is never optimal to exercise an American option prior to expiry, and s the additional rights confired to the American option are essentially worthless in this context.

For puts, American options are more valuable than European options, particularly so when stock price is lower.  The rational option holder exercises the American option when the stock price is sufficiently low - there is more to be gained by investing risk-free when there is not much room for a decrease in stock price.  At large stock prices, the two types of option approach the same value asymptotically.  As the time to expiry decreases, the optimal exercise price increases.

As the time to expiry decreases, the value of the options approach the known payoff function for both calls and puts, for both American and European options, as expected.


## Monte Carlo Methods - Options Pricing
In a Monte-Carlo program, the values of certain European options are calculated and compared with the analytic results as a test of the program.  Then, path-dependent options are investigated and their values evaluated.