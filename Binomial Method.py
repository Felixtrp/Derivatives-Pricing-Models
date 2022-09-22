# This program creates a binary tree modelling the price of a stock
# The price is dependent on interest rates, volatility and time
# Based on a p = 0.5 model

# -------------------------

# import modules
import numpy as np
import matplotlib.pyplot as plt

# calculate tree variables u and d
# These are the change in stock price with each step

def find_dt_u_d(r, sigma, T, steps):
    dt = T/steps
    A = np.exp((sigma**2)*dt) - 1
    B = np.exp(r*dt)
    u = B*(1+np.sqrt(A))
    d = B*(1-np.sqrt(A))
    return dt, u, d

# for a given time, steps - produce a tree
# specify S_0, r, sigma, T, steps
def produce_tree(S_0, r, sigma, T, steps):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    tree = []
    for i in range(steps+1):
        row = []
        for j in range(i+1):
            value = S_0*(u**j)*(d**(i-j))
            row.append(value)
        tree.append(row)
#        print(i, row)
#    print()
    return tree

# define a payoff for a european call
def euro_call(S, E):
    if S > E:
        payoff = S-E
    else:
        payoff = 0
    return payoff

# find the price of a euro call option
def euro_call_value(S_0, r, sigma, T, steps, E):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    tree = produce_tree(S_0, r, sigma, T, steps)
    tree_len = len(tree)
    final_row = tree[tree_len-1]
    payoff_row = []
    for value in final_row:
        pay_value = euro_call(value, E)
        payoff_row.append(pay_value)
    
    discount = np.exp(-r*dt)
    
#    print("Working backwards")
#    print("Starting", payoff_row)
    for i in range(steps):
        new_row = []
        for j in range(len(payoff_row)-1):
            new_value = discount*(0.5)*(payoff_row[j]+payoff_row[j+1])
            new_row.append(new_value)
#        print(new_row)
        payoff_row = new_row
    call_value = payoff_row[0]
#    print("CALL: ", call_value)
    return call_value
        



# A function that runs a load of bernoulli trials on calculated u and d values
# This checks that the results are as expected
# Behaviour is largely resolution independent above a critical step numbers - this is what we want
    
def plot_stock_sample(S_0, r, sigma, T, steps, trials):
    dt, u, d = find_dt_u_d(r, sigma, T, steps)
    
    for j in range(trials):
        y = [100]
        t = [0.0]
        
        S = 100
        t_0 = 0.0
        for i in range(steps):
            rand = np.random.random()
            if rand < 0.5:
                S *= u
            else:
                S *= d
            t_0 += dt
            y.append(S)
            t.append(t_0)
        
        plt.plot(t, y, c='k', lw=1)
    #plt.yscale('log')
    plt.show()

    
r = 0.04
sigma = 0.2
steps = 20
E = 120

S_0_list = np.linspace(0.01, 190, 200)

T = 10
C_list = []
for S_0 in S_0_list:
    call_value = euro_call_value(S_0, r, sigma, T, steps, E)
    print(call_value)
    C_list.append(call_value)
plt.plot(S_0_list, C_list, c='r')

T = 5
C_list = []
for S_0 in S_0_list:
    call_value = euro_call_value(S_0, r, sigma, T, steps, E)
    print(call_value)
    C_list.append(call_value)
plt.plot(S_0_list, C_list, c='b')

T = 1
C_list = []
for S_0 in S_0_list:
    call_value = euro_call_value(S_0, r, sigma, T, steps, E)
    print(call_value)
    C_list.append(call_value)
plt.plot(S_0_list, C_list, c='g')

T = 0.01
C_list = []
for S_0 in S_0_list:
    call_value = euro_call_value(S_0, r, sigma, T, steps, E)
    print(call_value)
    C_list.append(call_value)
plt.plot(S_0_list, C_list, c='k')


plt.show()


#trials = 300
#plot_stock_sample(S_0, r, sigma, T, steps, trials)

