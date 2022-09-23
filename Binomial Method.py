# This program uses a binary tree method to calculate the price of European and American options

### HOW IT WORKS ###
## Binary model of stock price.

# The time to expiry is broken into a number of discrete timesteps
# at each time step, the stock is modelled as having two possible motions - up or down.
# The probability that the stock price moves up (multiply by u>1.0) is p.
# The probability that the stock price moves down (multiply by d<1.0) is 1-p.
# p, u, d chosen to replicate mean and variance of a stock with known r, sigma.
# Two constraints, 3 unknowns => we have an underdefined problem.  Let p = 0.5 for simplicity.
# This sets unique values of u, d.

## Once this tree of stock prices is calculated, the pricing of options can begin.

# For European options, the process is straightforward.  The payoff for each possible stock price at expiry is calculated.
# These payoffs at expiry are identical to the price of the option at expiry.
# In the time step just prior to expiry, the value of the option is the discounted expected return.
# That is, to calculate the price of the option at a time (T-dt) - V(T-dt) - we consider the two possible paths along which it may evolve.
# WWe can call these V(T)_u - to which it evolves with probability p - and V(T)_d - to which it evolves with probability (1-p).
# The value V(T-dt)is then exp(-r*dt)*(p*V(T)_u) + ((1-p)*V(T)_d).
# The price of the option given every possible stock price at a time T-dt can be calculated in this way.
# The calculation then proceeds inductively, working backwards through the tree, until a price for the option at the current time is known.

# For American options, the process is not much more complicated.  The process proceeds as before, but this time the options holder has the right to early exercise.
# Each time the option price is calculated, therefore, there are two possible values:
#    1. The value of holding the option - equal to the weighted sum of future values just like European options.
#    2. The value of exercising the option early.
# A rational investor will choose whichever strategy provides greater benefit, and so this must be the price of the option to avoid arbitrage.

# The binomial model can only calculate prices for options that have values which are functions of stock price and time to expiry.
# To this model, a stock that moves up and down, or down and up, or remains constant, will all result in the same value for the options.
# Therefore, this model cannot be used to calucate path-dependent options (unless they can be reformulated in a path-independent way).

# -------------------------

# import modules
import numpy as np
import matplotlib.pyplot as plt

# Based on a p=0.5 binomial method.
# Calculate tree variables u and d
# These are the change in stock price with each step.

def find_dt_u_d(r, sigma, T, steps):
    dt = T/steps
    A = np.exp((sigma**2)*dt) - 1
    B = np.exp(r*dt)
    u = B*(1+np.sqrt(A))
    d = B*(1-np.sqrt(A))
    return dt, u, d

# For a given time, steps - produce a tree of possible stock prices.
# Specify S_0, r, sigma, T, steps
def produce_tree(S_0, r, sigma, T, steps):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    tree = []
    for i in range(steps+1):
        row = []
        for j in range(i+1):
            value = S_0*(u**j)*(d**(i-j))
            row.append(value)
        tree.append(row)
    return tree

# A function that runs a load of bernoulli trials on calculated u and d values
# This checks that the results are as expected to generate stock with correct drift and volatility.
# Behaviour is largely resolution independent above a critical step numbers - this is what we want
    
def plot_stock_sample(S_0, r, sigma, T, steps, trials):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    
    fig_1, axs_1 = plt.subplots(figsize=(12,8))
    title_string = "Binomial Tree of Stock Price Probabilities"
    fig_1.suptitle(title_string)

    subplot_title = r"$r = $" + str(r) + r", $\sigma = $" + str(sigma) + ", " + str(steps) + " steps"
    axs_1.set_title(subplot_title)

    for j in range(trials):
        S = [S_0]
        t = [0.0]
        
        S_now = S_0
        t_0 = 0.0
        for i in range(steps):
            rand = np.random.random()
            if rand < 0.5:
                S_now *= u
            else:
                S_now *= d
            t_0 += dt
            S_plot = S_now + (S_now*np.random.normal(0, 0.015)) # plotting with a tiny variation shows distribution more easily.
            S.append(S_plot)
            t.append(t_0)
        
        axs_1.plot(t, S, c='k', lw=0.1, alpha=0.8)
    
    axs_1.set_xlabel("Time")
    axs_1.set_ylabel("Stock Price")
    plt.show()


# Define a payoff function.
# types of options are "call", "put", "cash_or_nothing_call", "cash_or_nothing_put"
def payoff(S, E, option_type): # S = Stock Price, E = Exercise Price.
    if option_type == "call":
        if (S-E) > 0:
            payoff = S-E
        else:
            payoff = 0
        return payoff
    elif option_type == "put":
        if (E-S) > 0:
            payoff = E-S
        else:
            payoff = 0
        return payoff
    elif option_type == "cash_or_nothing_call":
        if (S-E) > 0:
            payoff = 10
        else:
            payoff = 0
        return payoff
    elif option_type == "cash_or_nothing_put":
        if (E-S) > 0:
            payoff = 10
        else:
            payoff = 0
        return payoff

# find the price of a European option.
def find_euro_option_value(S_0, r, sigma, T, steps, E, option_type):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    tree = produce_tree(S_0, r, sigma, T, steps)
    tree_len = len(tree)
    final_row = tree[tree_len-1]
    payoff_row = []
    for value in final_row:
        pay_value = payoff(value, E, option_type)
        payoff_row.append(pay_value)
    discount = np.exp(-r*dt)
    
    for i in range(steps):
        new_row = []
        for j in range(len(payoff_row)-1):
            new_value = discount*(0.5)*(payoff_row[j]+payoff_row[j+1])
            new_row.append(new_value)
        payoff_row = new_row
    euro_option_value = payoff_row[0]
    return euro_option_value


# find the price of a American option.
def find_amer_option_value(S_0, r, sigma, T, steps, E, option_type):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    tree = produce_tree(S_0, r, sigma, T, steps)
    tree_len = len(tree)
    final_row = tree[tree_len-1]
    payoff_row = []
    for value in final_row:
        pay_value = payoff(value, E, option_type)
        payoff_row.append(pay_value)
    discount = np.exp(-r*dt)
    
    s_f_list = []

    for i in range(steps):
        tree_row = tree[(tree_len-2)-i]
        new_row = []
        for j in range(len(payoff_row)-1):
            hold_value = discount*(0.5)*(payoff_row[j]+payoff_row[j+1])
            tree_value = tree_row[j]
            exercise_value = payoff(tree_value, E, option_type)
            if exercise_value>hold_value:
                exercise=True
            else:
                exercise=False
            new_value = max(hold_value, exercise_value)
            new_row.append(new_value)
        payoff_row = new_row
    amer_option_value = payoff_row[0]
    return amer_option_value, exercise
        

if __name__ == "__main__":
    # Specify some parameters of interest
    r = 0.20 # interest rate
    sigma = 0.2 # volatility
    S_0 = 100 # intial stock price
    # Model paramters
    steps = 10 # binomial steps

    # # Plot the binary tree to demonstrate how the stock price is being modelled.
    T = 3.0 # time horizon (time to expiry)
    trials = 1000 # how many lines to show in the plot
    plot_stock_sample(S_0, r, sigma, T, steps, trials)
    

    ### Calculate the price of the options
    # Specify some parameters of interest
    r = 0.04 # interest rate
    sigma = 0.2 # volatility

    # Model paramters
    steps = 40 # binomial steps
    E = 120 # strike price

    S_0_list = np.linspace(0.0, 300, 2000) # the possible current stock prices
    
    ### Produce a figure showing calls and puts
    fig_2, axs_2 = plt.subplots(4, 2, sharex=True, figsize=(12,8))

    title_string = "Vales of Options Calculated Using a Binomial Method - " + r"$r = $" + str(r) + r", $\sigma = $" + str(sigma) + r", $E = $" + str(E)
    fig_2.suptitle(title_string)
    # Calls first
    option_type = "call" # types are "call", "put", "cash_or_nothing_call", "cash_or_nothing_put"

    # Increment through timesteps
    T = 10 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[0][0].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[0][0].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[0][0].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[0][0].text(0.05, .7,title_string,
            transform=axs_2[0][0].transAxes, fontsize=10)
    

    ## Timestep 2
    T = 5 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[1][0].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[1][0].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[1][0].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[1][0].text(0.05, .7,title_string,
            transform=axs_2[1][0].transAxes, fontsize=10)

    ## Timestep 3
    T = 2 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[2][0].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[2][0].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[2][0].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[2][0].text(0.05, .7,title_string,
            transform=axs_2[2][0].transAxes, fontsize=10)
    
    ## Timestep 4
    T = 0 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[3][0].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[3][0].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[3][0].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[3][0].text(0.05, .7,title_string,
            transform=axs_2[3][0].transAxes, fontsize=10)

    # Now with Puts
    # Calls first
    option_type = "put" # types are "call", "put", "cash_or_nothing_call", "cash_or_nothing_put"

    # Increment through timesteps
    T = 10 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[0][1].text(0.25, .7,title_string,
            transform=axs_2[0][1].transAxes, fontsize=10)

    #plot euro option
    axs_2[0][1].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[0][1].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[0][1].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")

    ## Timestep 2
    T = 5 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[1][1].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[1][1].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[1][1].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[1][1].text(0.25, .7,title_string,
            transform=axs_2[1][1].transAxes, fontsize=10)

    ## Timestep 3
    T = 2 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[2][1].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[2][1].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[2][1].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[2][1].text(0.25, .7,title_string,
            transform=axs_2[2][1].transAxes, fontsize=10)

    
    ## Timestep 4
    T = 0 # to,e tp expiry
    V_E_list = [] # European voption value

    S_0_hold_list = []
    V_A_hold_list = []
    
    S_0_exercise_list = []
    V_A_exercise_list = []
    
    for S_0 in S_0_list:
        euro_option_value = find_euro_option_value(S_0, r, sigma, T, steps, E, option_type)
        amer_option_value, exercise = find_amer_option_value(S_0, r, sigma, T, steps, E, option_type)
        V_E_list.append(euro_option_value)
        if exercise:
            V_A_exercise_list.append(amer_option_value)
            S_0_exercise_list.append(S_0)
        else:
            V_A_hold_list.append(amer_option_value)
            S_0_hold_list.append(S_0)
    
    #plot euro option
    axs_2[3][1].plot(S_0_list, V_E_list, c='b', label="European Option")

    # plot american option
    axs_2[3][1].plot(S_0_hold_list, V_A_hold_list, c='r', label = "American Option (Held)")
    if len(S_0_exercise_list)>0:
        axs_2[3][1].plot(S_0_exercise_list, V_A_exercise_list, '--', c='r', label = "American Option (Exercised)")
    
    t_title = str(T)
    title_string = "t = " + t_title
    axs_2[3][1].text(0.25, .7,title_string,
            transform=axs_2[3][1].transAxes, fontsize=10)
    
    #####

    axs_2[0][0].set_title("Call Options")
    axs_2[0][1].set_title("Put Options")

    axs_2[0][1].legend()

    axs_2[3][0].set_xlabel("Stock Price")
    axs_2[3][1].set_xlabel("Stock Price")
    
    plt.show()
