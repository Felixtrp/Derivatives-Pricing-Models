## This program computes the price of 'exotic' options using a Monte-Carlo method
# ---------------------------------

# import modules
from re import A
import numpy as np
import matplotlib.pyplot as plt
from GeomStockPrice import find_stock_price # a function that produces a random stock price

# define the payoff for some exotic function
# try a path-dependent functio
# an 'Asian' option has a payoff that is determined by its average value between issue and expiry

# define a function to calculate the average - different options use different definitions of 'average' - we will stick with arithmetic average
# we will assume an equal time step in the data
def find_average(S):
    avg_S = np.mean(S)
    return avg_S

# an Asian call has a price at expiry equal to the maximum of either the average-strike or zero.
def asian_call_payoff(S, E):
    avg_S = find_average(S)
    if avg_S>E:
        payoff = avg_S-E
    else:
        payoff = 0
    return payoff

# Another exotic option - the 'lookback' option - an option to buy the stock at the highest price
# in the time interval
def lookback_call_payoff(S, E):
    max_S = max(S)
    if max_S>E:
        payoff = max_S-E
    else:
        payoff = 0
    return payoff


# let's run a few tests
if __name__ == "__main__":

    ## Calculate the price of an Asian call option at different times and stock prices

    r = 0.1
    sigma = 0.1
    steps = 25
    trials = 500
    sqrt_trials = np.sqrt(trials)

    E = 130
    S_0_list = np.linspace(0.01, 200, 10)

    def make_asian_call_plot(S_0_list, T, color_name, r, sigma, steps, E):
        mean_asian_price = []
        err_asian_price = []
        discount = np.exp(-r*T)
        for S_0 in S_0_list:
            asian_price = []
            for i in range(trials):
                S, t = find_stock_price(S_0, r, sigma, T, steps)
                asian_call_at_expiry = asian_call_payoff(S,E)
                asian_price.append(asian_call_at_expiry*discount)
            mean_price = np.mean(asian_price)
            err_price = 1.96*np.std(asian_price)/sqrt_trials
            mean_asian_price.append(mean_price)
            err_asian_price.append(err_price)
            print(S_0)

        plt.errorbar(S_0_list, mean_asian_price, yerr=err_asian_price, fmt='none',
        color=color_name, capsize=5, elinewidth=2, markeredgewidth=2)

        label_name = "T = " + str(T)
        plt.plot(S_0_list, mean_asian_price, c=color_name, label=label_name)
    
    fig, ax = plt.subplots(1,1)

    fig.suptitle("Asian Call Option Prices - Calculated using a Monte-Carlo method")
    
    title_string = r"$r = $" + str(r) + r", $\sigma = $" + str(sigma) + r", $E = $" + str(E)
    ax.set_title(title_string, fontsize=15)
    ax.set_xlabel("Stock Price")
    ax.set_ylabel("Option Price")
    

    T = 10.0
    color_name = "black"
    make_asian_call_plot(S_0_list, T, color_name, r, sigma, steps, E)
    
    T = 5.0
    color_name = "blue"
    make_asian_call_plot(S_0_list, T, color_name, r, sigma, steps, E)

    T = 2.0
    color_name = "red"
    make_asian_call_plot(S_0_list, T, color_name, r, sigma, steps, E)

    T = 0.0
    color_name = "green"
    make_asian_call_plot(S_0_list, T, color_name, r, sigma, steps, E)

    ax.legend()

    plt.show()

    #####
    # now calculate the price for a lookback call

    r = 0.03
    sigma = 0.2
    steps = 1000
    trials = 1000
    sqrt_trials = np.sqrt(trials)

    E = 130
    S_0_list = np.linspace(0.01, 200, 10)

    def make_lookback_call_plot(S_0_list, T, color_name, r, sigma, steps, E):
        mean_lookback_price = []
        err_lookback_price = []
        discount = np.exp(-r*T)
        for S_0 in S_0_list:
            lookback_price = []
            for i in range(trials):
                S, t = find_stock_price(S_0, r, sigma, T, steps)
                lookback_call_at_expiry = lookback_call_payoff(S,E)
                lookback_price.append(lookback_call_at_expiry*discount)
            mean_price = np.mean(lookback_price)
            err_price = 1.96*np.std(lookback_price)/sqrt_trials
            mean_lookback_price.append(mean_price)
            err_lookback_price.append(err_price)
            print(S_0)

        plt.errorbar(S_0_list, mean_lookback_price, yerr=err_lookback_price, fmt='none',
        color=color_name, capsize=5, elinewidth=2, markeredgewidth=2)

        label_name = "T = " + str(T)
        plt.plot(S_0_list, mean_lookback_price, c=color_name, label=label_name)
    
    fig_new, ax_new = plt.subplots(1,1)

    fig_new.suptitle("Lookback Call Option Prices - Calculated using a Monte-Carlo method")
    
    title_string = r"$r = $" + str(r) + r", $\sigma = $" + str(sigma) + r", $E = $" + str(E)
    ax_new.set_title(title_string, fontsize=15)
    ax_new.set_xlabel("Stock Price")
    ax_new.set_ylabel("Option Price")
    
    T = 10.0
    color_name = "black"
    make_lookback_call_plot(S_0_list, T, color_name, r, sigma, steps, E)
    
    T = 5.0
    color_name = "blue"
    make_lookback_call_plot(S_0_list, T, color_name, r, sigma, steps, E)
    
    T = 2.0
    color_name = "red"
    make_lookback_call_plot(S_0_list, T, color_name, r, sigma, steps, E)
    
    T = 1.0
    color_name = "green"
    make_lookback_call_plot(S_0_list, T, color_name, r, sigma, steps, E)

    ax_new.legend()
    
    plt.show()
    
    