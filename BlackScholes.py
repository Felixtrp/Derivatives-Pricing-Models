## This program calculate options prices according to the Black-Scholes equation
## European calls and puts have exact formulations which will be produced.
## Other European options can stil be found with numerical solutions to the Black-Scholes equation.

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

### CALLS AND PUTS (ANALYTIC SOLUTIONS)
# the value of a European call/put is a function of:
# S - Current stock price
# t - time to expiry
# r - risk-free interest rate
# sigma - stock volatility
# E - Exercise price

# Analytic solution to European call
def european_call(S, t, r, sigma, E):
    d_1 = ((np.log(S/E)) + ((r + (sigma**2)/2)*t))/(sigma*np.sqrt(t))
    d_2 = d_1 - (sigma*np.sqrt(t))
    C_1 = norm.cdf(d_1)*S
    C_2 = norm.cdf(d_2)*E*np.exp(-r*t)
    C = C_1 - C_2    
    return C

# Analytic solution to European put
def european_put(S, t, r, sigma, E):
    d_1 = ((np.log(S/E)) + ((r + (sigma**2)/2)*t))/(sigma*np.sqrt(t))
    d_2 = d_1 - (sigma*np.sqrt(t))
    P_1 = norm.cdf(-d_1)*S
    P_2 = norm.cdf(-d_2)*E*np.exp(-r*t)
    P = P_2 - P_1    
    return P

# Make a plot of European call prices
def make_call_plot(t, r, sigma, color_name):
    S_list = np.linspace(50, 200)
    C_list = []

    for S in S_list:
        C = european_call(S, t, r, sigma, E)
        C_list.append(C)
    label_name = "T = " + str(t)
    plt.plot(S_list, C_list, c=color_name, label=label_name)


# Make a plot of European put prices
def make_put_plot(t, r, sigma, color_name):
    S_list = np.linspace(50, 200)
    P_list = []

    for S in S_list:
        P = european_put(S, t, r, sigma, E)
        P_list.append(P)
    label_name = "T = " + str(t)
    plt.plot(S_list, P_list, c=color_name, label=label_name)

#### OTHER EUROPEAN OPTIONS
# For European options other than calls or puts, we can solve the Black-Scholes equation numerically
# Define a payoff function

# EXAMPLE: an option that pays out only if the stock expires in a certain window
def payoff(S):
    E = 110
    B = 120
    if S > B:
        payoff = 0
    elif S>E:
        payoff = 10
    else:
        payoff = 0
    return payoff

# Now, construct a grid of points in the S, T plane
# Rearranging BS, we obtain dVdt in terms of the other variables
# dVdt = r*V - r*S*dVdS - 1/2*sigma**2*d2VdS2
# A solution can then be found via the following steps:
# 1. Calculate payoff at expiry V_expiry = payoff(S)
# 2. Calculate LHS of equation above for this time.
# 3. THis give RHS.
# 4. Step backwards a small amount in time.
# 5. Repeat to desired time.

# make some formulae to calculate derivatives
def find_dVdS(V_list, S_list):
    dVdS_list = []
    for i in range(len(V_list)-1):
        V_1 = V_list[i]
        V_2 = V_list[i+1]
        S_1 = S_list[i]
        S_2 = S_list[i+1]
        dVdS = (V_2-V_1)/(S_2-S_1)
        dVdS_list.append(dVdS)
    # we need to append a final value to maintain the length of dVdS
    # linear interp
    list_len = len(dVdS_list)
    deltadVdS = (dVdS_list[list_len-1]-dVdS_list[list_len-2])
    deltaS = (S_list[list_len-2] - S_list[list_len-3])
    gradient = deltadVdS/deltaS
    final_value = dVdS_list[list_len-1] + (S_list[-1] - S_list[-2])*gradient
    dVdS_list.append(final_value)
    return dVdS_list

def find_d2VdS2(V_list, S_list):
    d2VdS2_list = []
    for i in range(1, len(V_list)-1):
        V_minus = V_list[i-1]
        V = V_list[i]
        V_plus = V_list[i+1]
        S_1 = S_list[i]
        S_2 = S_list[i+1]
        d2VdS2 = (V_minus-(2*V) + V_plus)/(S_2-S_1)
        d2VdS2_list.append(d2VdS2)
    # we need to append an initial and a final value to maintain the length of dVdS
    # linear interp
    list_len = len(d2VdS2_list)
    # final value
    deltad2VdS2 = (d2VdS2_list[list_len-1]-d2VdS2_list[list_len-2])
    deltaS = (S_list[list_len-2] - S_list[list_len-3])
    gradient = deltad2VdS2/deltaS
    final_value = d2VdS2_list[list_len-1] + (S_list[-1] - S_list[-2])*gradient
    d2VdS2_list.append(final_value)
    
    # initial value
    deltad2VdS2 = (d2VdS2_list[1]-d2VdS2_list[0])
    deltaS = (S_list[1] - S_list[0])
    gradient = deltad2VdS2/deltaS
    initial_value = d2VdS2_list[0] - (S_list[1] - S_list[0])*gradient
    d2VdS2_list.insert(0, initial_value)
    
    return d2VdS2_list

# Calculate the payoff at expiry for a range of tock prices
def find_V_expiry(S_list, payoff):
    V_expiry = []
    for S in S_list:
        V = payoff(S)
        V_expiry.append(V)
    return V_expiry

# For a given list of V, S, r, sigma - calculate dVdt
def find_dVdt(V_list, S_list, r, sigma):
    dVdt_list = []
    dVdS_list = find_dVdS(V_list, S_list)
    d2VdS2_list = find_d2VdS2(V_list, S_list)
    for i in range(len(V_list)):
        V= V_list[i]
        S = S_list[i]
        dVdS = dVdS_list[i]
        d2VdS2 = d2VdS2_list[i]
        
        dVdt = 0
        dVdt += r*V
        dVdt -= r*S*dVdS
        dVdt -= 0.5*sigma*sigma*S*d2VdS2

        dVdt_list.append(dVdt)

    return dVdt_list
    
# construct a function that increments V a small amount (backwards)
def update_V(V_list, dVdt_list, dt):
    new_V_list = []
    for i in range(len(V_list)):
        V = V_list[i]
        dVdt = dVdt_list[i]
        dV = dVdt*dt
        new_V = V - dV # we are iterating backwards
        new_V_list.append(new_V)
    return new_V_list

# Now put it all together - for n steps for size dt
def find_option_value(S_list, r, sigma, steps, dt):
    V_expiry = find_V_expiry(S_list, payoff)
    
    V_data = [V_expiry]
    t_list = [0.0]
    
    V_now = V_expiry
    t_now = 0.0
    for i in range(steps):
        dVdt_list = find_dVdt(V_now, S_list, r, sigma)
        V_new = update_V(V_now, dVdt_list, dt)
        t_new = t_now + dt

        V_data.append(V_new)
        t_list.append(t_new)

        V_now = V_new
        t_now = t_new
    
    return V_data, t_list







if __name__ == "__main__":
    # specify some conditions for the stock
    r = 0.05 # interest rate
    sigma = 0.1 # volatility
    E = 120 # strike price

    ### European Calls ###
    # make a few plots at different times-to-expiy
    fig_1, axs_1 = plt.subplots(1, 1)

    title_string = "Value of European Call Options Calculated Using The Black-Scholes Formula - "
    fig_1.suptitle(title_string)

    subtitle_string = r"$r = $" + str(r) + r", $\sigma = $" + str(sigma) + r", $E = $" + str(E)
    axs_1.set_title(subtitle_string)
    

    t = 1.00
    color_name = 'blue'
    make_call_plot(t, r, sigma, color_name)
        
    t = 0.50
    color_name = 'red'
    make_call_plot(t, r, sigma, color_name)
        
    t = 0.01
    color_name = 'green'
    make_call_plot(t, r, sigma, color_name)

    plt.xlabel("Stock Price")
    plt.ylabel("Option Price")
    plt.legend()
    plt.show()

    ######################################
    
    ### European Puts ###
    # make a few plots at different times-to-expiy
    fig_2, axs_2 = plt.subplots(1, 1)

    title_string = "Value of European Put Options Calculated Using The Black-Scholes Formula - "
    fig_2.suptitle(title_string)

    subtitle_string = r"$r = $" + str(r) + r", $\sigma = $" + str(sigma) + r", $E = $" + str(E)
    axs_2.set_title(subtitle_string)
    
    t = 1.00
    color_name = 'blue'
    make_put_plot(t, r, sigma, color_name)
        
    t = 0.50
    color_name = 'red'
    make_put_plot(t, r, sigma, color_name)
        
    t = 0.01
    color_name = 'green'
    make_put_plot(t, r, sigma, color_name)
    
    
    plt.xlabel("Stock Price")
    plt.ylabel("Option Price")
    plt.legend()
    plt.show()

    ################
    ## Other European Options
    # Stock paramters
    r = 0.05 # interest rate
    sigma = 0.1 # volatility

    # Algorithm parameters
    S_list = np.linspace(50, 150, 400)
    dt = 0.01
    steps = 1000

    V_data, t_list = find_option_value(S_list, r, sigma, steps, dt)

    index = 0
    V_list = V_data[index]
    t = t_list[index]
    
    t_title = '%s' % float('%.1g' % t)
    label_name = "t = " + t_title
    plt.plot(S_list, V_list, label=label_name)

    
    index = 300
    V_list = V_data[index]
    t = t_list[index]
    
    t_title = '%s' % float('%.1g' % t)
    label_name = "t = " + t_title
    plt.plot(S_list, V_list, label=label_name)

    
    index = 600
    V_list = V_data[index]
    t = t_list[index]
    
    t_title = '%s' % float('%.1g' % t)
    label_name = "t = " + t_title    
    plt.plot(S_list, V_list, label=label_name)
    
    title_string = "The value of a European option that pays out 10 if the stock price expires between 120 and 150 - r = " + str(r) + r", $\sigma = $" + str(sigma) 
    plt.title(title_string)
    
    plt.xlabel("Stock Price")
    plt.ylabel("Option Value")

    plt.legend()
    plt.show()