# Stock price simulator, based on geometric brownian motion
# This will later be used for Monte-Carlo options pricing models
# The program __main__ analyses the simulation results, demonstrating that they match results derived from theory (Ito Calculus).

#----------------------------

# import modules
import numpy as np
import matplotlib.pyplot as plt
import math

# given S_0, r, sigma, time horizon and steps, generate a stock price simulation
# based on geometric Brownian motion

def find_stock_price(S_0, r, sigma, T, steps):
    # find timestep
    dt = T/steps
    
    # initialise lists
    S = [S_0]
    t = [0.0]
    
    S_now = S_0
    t_now = 0.0
    
    # perform simulation
    for i in range(steps):
        drift = r*S_now*dt # drift component
        vol = sigma*S_now*np.random.normal(0, np.sqrt(dt)) # random walk component
        dS = drift + vol # total change
        
        # updae current values
        S_now += dS
        t_now += dt
        
        # update lists
        S.append(S_now)
        t.append(t_now)
    
    return S, t

# get analytic solution for probability density
# based on the results derived from Ito calculus - continuous random walk of geometric brownian motion

# the probability density function
def p_func(S, S_0, r, sigma, t):
    factor = 1/(sigma*S*np.sqrt(2*np.pi*t))
    exponent = -( (np.log(S/S_0) - ((r-0.5*sigma*sigma)*t))**2 )/(2*sigma*sigma*t)
    p = factor*np.exp(exponent)
    return p
    
# evaluating the probability density function of a specified range of values
def analytic_stock_prob(S_range, S_0, r, sigma, t):
    p = []
    for S in S_range:
        p_value = p_func(S, S_0, r, sigma, t)
        p.append(p_value)
    return p

## Main program - simulate results and analyse
if __name__ == "__main__":    
    ## Specify input conditions for stock price
    S_0 = 100 # intial price
    r = 0.15 # interest/drift
    sigma = 0.05 # volatility
    T = 5.0 # time horizon
    
    ## specify computational parameters
    steps = 100 # time steps
    trials = 10000 # number of simulations
    
    # note which time points we want to observe for plots later on
    # (It's faster to do this as the simulations are produced, but could be done after)
    index_list = [10, 30, 60, 90]
    
    # initialise list to collect results
    S_data = []
    
    # run simulation
    for i in range(trials):
        S, t = find_stock_price(S_0, r, sigma, T, steps)
        S_data.append(S) # record results
    
    # calculate deciles, quartiles and medians
    # the position in the sorted results at which they occur
    d_1_index = int(math.floor(trials/10))
    q_1_index = int(math.floor(trials/4))
    m_index = int(math.floor(2*trials/4))
    q_3_index = int(math.floor(3*trials/4))
    d_9_index = int(math.floor(9*trials/10))
    
    # initialise lists
    d_1 = [S_0]
    q_1 = [S_0]
    median = [S_0]
    q_3 = [S_0]
    d_9 = [S_0]
    
    # find all simulation values at a specific time
    # sort the results
    # record the deciles, quartiles and median
    for i in range(steps):
        time_list = []
        for j in range(trials):
            S = S_data[j]
            time_value = S[i]
            time_list.append(time_value)
        time_list.sort() # sort results
        d_1.append(time_list[d_1_index])
        q_1.append(time_list[q_1_index])
        median.append(time_list[m_index])
        q_3.append(time_list[q_3_index])
        d_9.append(time_list[d_9_index])
        
    
    #####################
    ### Figure 1 ###
    
    # produce figure showing results of simulation
    fig_1, axs_1 = plt.subplots(1, 1, figsize=(12,8))
    
    fig_1.suptitle("Stock Price Simulation Results - Geometric Brownian Motion", fontsize=20)
    
    title_string = r"$S_0 = $" + str(S_0) + r", $r = $" + str(r) + r", $\sigma = $" + str(sigma)
    axs_1.set_title(title_string, fontsize=15)
    
    # plot some simulation results
    # (we don't need all of them)
    for i in range(300):
        S = S_data[i]
        axs_1.plot(t, S, c='r', lw=0.2)
    
    axs_1.plot([0], [S_0], c='r', lw=2, label="Simulation Instance") # for legend
    
    # plot deciles etc.
    axs_1.plot(t, d_1, '--', c='k', lw=2, label="Deciles 1/9")
    axs_1.plot(t, q_1, '-.', c='k', lw=3, label="Quartiles 1/3")
    axs_1.plot(t, median, c='k', lw=4, label="Median")
    axs_1.plot(t, q_3, '-.', c='k', lw=3)
    axs_1.plot(t, d_9, '--', c='k', lw=2)
    
    # legend
    axs_1.legend(fontsize=15)
    
    # set plot appearance
    axs_1.set_xlabel("Time", fontsize=15)
    axs_1.set_ylabel("Stock Price", fontsize=15)
    
    axs_1.tick_params(axis='both', which='major', labelsize=15)
    axs_1.tick_params(axis='both', which='minor', labelsize=8)

    plt.show()
    
    #########################
    ### Figure 2 ###
    
    # produce figure comparing distributions over time
    # using the variable axs for multiple Axes
    fig_2, axs_2 = plt.subplots(4, 1, sharex=True, figsize=(8,8))
    
    fig_2.suptitle("Probability Density of Future Stock Prices", fontsize=20)
    
    S_range = np.linspace(0.1, 400, 1000) # the range ver which we care about evaluating the analytic function
    
    # at a specified time step, record simulation results and analytic distribution
    for i in range(len(index_list)):
        index = index_list[i]
        t_index = t[index]
        
        # simulation results
        S_exp_index = []
        for j in range(trials):
            S_exp_index.append(S_data[j][index])
        
        # analytic results
        p = analytic_stock_prob(S_range, S_0, r, sigma, t_index)
        
        # plot both - exp. histogram and analytic pdf curve
        axs_2[i].hist(S_exp_index, density=True, bins=100, label="Simulation Results")
        axs_2[i].plot(S_range, p, c='k', lw=4, label="Theoretical Prediction")
        
        t_title = '%s' % float('%.1g' % t_index)
        
        title_string = "t = " + t_title
        
        axs_2[i].text(0.05, .7,title_string,
            transform=axs[i].transAxes, fontsize=15)
    
    # Plot appearances
    title_string = r"$S_0 = $" + str(S_0) + r", $r = $" + str(r) + r", $\sigma = $" + str(sigma)
    
    axs_2[0].set_title(title_string, fontsize=15)
    axs_2[0].legend(fontsize=15)
    axs_2[3].set_xlabel("Stock Price", fontsize=15)
    
    axs_2[0].tick_params(axis='y', which='major', labelsize=12)
    axs_2[1].tick_params(axis='y', which='major', labelsize=12)
    axs_2[2].tick_params(axis='y', which='major', labelsize=12)
    axs_2[3].tick_params(axis='y', which='major', labelsize=12)
    
    axs_2[3].tick_params(axis='x', which='major', labelsize=15)
    plt.xlim([50, 300])
    plt.show()