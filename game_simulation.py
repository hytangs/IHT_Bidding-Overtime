
"""
Structural Auction Model Simulator
- for Auction with Bidding Mechanisms Model
- Section 3 of the IHT Final Report

Parameters and pre-tuned values as in Section 3.3:
    ev1_i: initial expected valuation for bidder 1 = 10
    ev2_i: initial expected valuation for bidder 2 = 10
    k: assigned overtime / countdown policy = 10
    p_learn: probability of learning = 0.6
    e_i: markup over valuation learning = 3
    gamma_i: attention cost of bidder side = 0.0003
    theta: deterministic bound of decision = 0.8
    p_hold: probability of snipping = 0.1
    markup_ah: auction house markup over winning price = 0.24
    gamma_ah: auction house duration cost = 0.0005

Guide for model simulation:

full_model(.model_params) performs one round of simulation
    takes any of the above parameters.
    returns: full bidding records, last_bidder (1 or 2), p*, t*, auction house profit

monte_carlo(n=1000, .model_params) performs Monte Carlo simulation
    takes any of the above parameters and:
    n: rounds of Monte Carlo simulation
    returns: mean P*, mean t*, mean auction house profit

find_k(n=1000, .model_params) finds the optimal policy k by price or profit
    takes any of the above parameters and:
    n: rounds of Monte Carlo simulation
    returns: best policy k by P*, value of such P*; best policy k by profit, value of such profit

draw_k(n=1000, .model_params) plots the relationship of price, profits and k.
    takes any of the above parameters and:
    n: rounds of Monte Carlo simulation
    returns: 2 dimension plot: P* ~ k and Profit ~ k

k_plane(ev1_range=(2, 30), ev2_range=(2, 30), .model_params) plots hyperplane of initial valuations and optimal k.
    takes any of the above parameters (excluding ev1_i and ev2_i) and:
    ev1_range: range of initial expected valuation for bidder 1
    ev2_range: range of initial expected valuation for bidder 2
    returns: hyperplane of ev1, ev2 and k.

prob_learning_hyperplane_plot(ev1=10, ev2=10, k_range) plots hyperplane of p_learn, price, and k for Section 6.2.
    takes initial valuations for bidder 1 and bidder 2.
    k_range: range of policies k to be evaluated =(1, 16).
    returns: hyperplane of k, p_learn, and auction house profit.

"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# model functions
def full_model(
        ev1_i=10,
        ev2_i=10,
        k=10,
        p_learn=0.6,
        e_i=3,
        gamma_i=0.0003,
        theta=0.8,
        p_hold=0.1,
        markup_ah=0.24,
        gamma_ah=0.0005
):
    # initialize auction
    t = 0
    p = 0
    ev1 = ev1_i
    ev2 = ev2_i
    k_remain = k
    terminate = False
    last_bidder = None

    # add list of bidding history (p, t, bidder)
    record = []

    # auction iteration
    while not terminate:
        t += 1

        if last_bidder != 1:
            # calculate ev1 & pi1
            if theta * ev1 >= p + 1:
                pass
            else:
                learning = np.random.binomial(1, p_learn)
                ev1 = (1 - learning) * ev1 + learning * (p + 1 + np.random.poisson(e_i))
            pi1 = ev1 - (p + 1) - gamma_i * (t ** 2)

            # calculate s1
            if pi1 <= 0:
                s1 = 0
            elif pi1 >= theta * ev1 and pi1 >= 0:
                s1 = 1
            else:
                urgency = 1 / np.log(k_remain + 2)
                value = np.log(pi1 + 1)
                snipping = p_hold
                s1 = min(urgency * value, 1) * (1 - snipping)
        else:
            # one bidder won't continuously place bids
            s1 = 0
            pi1 = ev1 - (p + 1) - gamma_i * (t ** 2)

        if last_bidder != 2:
            # calculate ev2 & pi2
            if theta * ev2 >= p + 1:
                pass
            else:
                learning = np.random.binomial(1, p_learn)
                ev2 = (1 - learning) * ev2 + learning * (p + 1 + np.random.poisson(e_i))
            pi2 = ev2 - (p + 1) - gamma_i * (t ** 2)

            # calculate s2
            if pi2 <= 0:
                s2 = 0
            elif pi2 >= theta * ev2 and pi2 >= 0:
                s2 = 1
            else:
                urgency = 1 / np.log(k_remain + 2)
                value = np.log(pi2 + 1)
                snipping = p_hold
                s2 = min(urgency * value, 1) * (1 - snipping)
        else:
            # one bidder won't continuously place bids
            s2 = 0
            pi2 = ev2 - (p + 1) - gamma_i * (t ** 2)

        # bernoulli by s1 and s2
        b1 = np.random.binomial(1, s1)
        b2 = np.random.binomial(1, s2)
        # when needed, to print the per-second dynamics
        # print(p, t, ev1, ev2, pi1, pi2, s1, s2, b1, b2, k_remain, last_bidder)

        # register successful bids
        if b1 == 1 and b2 == 1:
            last_bidder = np.random.binomial(1, 0.5) + 1
            p += 1
            record.append((p, t, last_bidder))
            k_remain = k
        elif b1 == 1 and b2 == 0:
            last_bidder = 1
            p += 1
            record.append((p, t, 1))
            k_remain = k
        elif b1 == 0 and b2 == 1:
            last_bidder = 2
            p += 1
            record.append((p, t, 2))
            k_remain = k
        else:
            k_remain -= 1

        # check terminate condition
        if k_remain == 0:
            terminate = True

    # calculate auction house profit
    ah_profit = markup_ah * p - gamma_ah * (t ** 2)
    return record, last_bidder, p, t, ah_profit


# n times auction simulation on given parameters
def monte_carlo(
        n=1000,
        ev1_i=10,
        ev2_i=10,
        k=10,
        p_learn=0.6,
        e_i=3,
        gamma_i=0.0003,
        theta=0.8,
        p_hold=0.1,
        markup_ah=0.24,
        gamma_ah=0.0005
):
    p_list = []
    t_list = []
    ah_list = []
    for i in range(n):
        outcome = full_model(
            ev1_i,
            ev2_i,
            k,
            p_learn,
            e_i,
            gamma_i,
            theta,
            p_hold,
            markup_ah,
            gamma_ah
        )
        p_list.append(outcome[2])
        t_list.append(outcome[3])
        ah_list.append(outcome[4])
    return np.mean(p_list), np.mean(t_list), np.mean(ah_list)


# find best k by highest P* and profit
def find_k(
        n=1000,
        ev1_i=10,
        ev2_i=10,
        p_learn=0.6,
        e_i=3,
        gamma_i=0.0003,
        theta=0.8,
        p_hold=0.1,
        markup_ah=0.24,
        gamma_ah=0.0005
):
    best_k_p = None
    best_p = 0
    best_p_list = None
    best_k_profit = None
    best_profit = -float('inf')
    best_profit_list = None

    for k in range(1, 20):
        p, t, profit = monte_carlo(
            n,
            ev1_i,
            ev2_i,
            k,
            p_learn,
            e_i,
            gamma_i,
            theta,
            p_hold,
            markup_ah,
            gamma_ah
        )

        if p > best_p:
            best_k_p = k
            best_p = p
            best_p_list = (p, t, profit)

        if profit > best_profit:
            best_k_profit = k
            best_profit = profit
            best_profit_list = (p, t, profit)

    return best_k_p, best_p_list, best_k_profit, best_profit_list


# draw the chart of P* and profit w.r.t policy k
def draw_k(
        n=1000,
        ev1_i=10,
        ev2_i=10,
        p_learn=0.6,
        e_i=3,
        gamma_i=0.0003,
        theta=0.8,
        p_hold=0.1,
        markup_ah=0.24,
        gamma_ah=0.0005,
        k_range=(1, 30)
):
    k_values = list(range(k_range[0], k_range[1] + 1))
    p_values = []
    profit_values = []

    for k in k_values:
        p, t, profit = monte_carlo(n, ev1_i, ev2_i, k, p_learn, e_i, gamma_i, theta, p_hold, markup_ah,
                                   gamma_ah)
        p_values.append(p)
        profit_values.append(profit)

    plt.figure(figsize=(10, 5))
    ax1 = sns.lineplot(x=k_values, y=p_values, label='p', marker='o')
    ax2 = ax1.twinx()
    sns.lineplot(x=k_values, y=profit_values, ax=ax2, label='profit', marker='x', color='r')

    ax1.set_xlabel('k')
    ax1.set_ylabel('p', color='b')
    ax2.set_ylabel('Profit', color='r')
    plt.title('Simulation of Price and Auction House Profit given k')
    plt.grid()
    plt.show()


# hyperplane of optimal k policies by range of initial evs
def k_plane(
        ev1_range=(2, 30),
        ev2_range=(2, 30),
        n=1000,
        p_learn=0.6,
        gamma_i=0.0003,
        theta=0.8,
        p_hold=0.1,
        markup_ah=0.24,
        gamma_ah=0.0005
):
    ev1_values = np.arange(ev1_range[0], ev1_range[1] + 1, 2)
    ev2_values = np.arange(ev2_range[0], ev2_range[1] + 1, 2)
    k_optimal = np.zeros((len(ev1_values), len(ev2_values)))

    for i, ev1_i in enumerate(ev1_values):
        for j, ev2_i in enumerate(ev2_values):
            best_k_p, _, best_k_profit, _ = find_k(
                n=n,
                ev1_i=ev1_i,
                ev2_i=ev2_i,
                p_learn=p_learn,
                gamma_i=gamma_i,
                theta=theta,
                p_hold=p_hold,
                markup_ah=markup_ah,
                gamma_ah=gamma_ah
            )
            print(i, j)
            k_optimal[i, j] = best_k_profit

    ev1_mesh, ev2_mesh = np.meshgrid(ev1_values, ev2_values)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(ev1_mesh, ev2_mesh, k_optimal, cmap='viridis')
    ax.set_xlabel('ev1_i')
    ax.set_ylabel('ev2_i')
    ax.set_zlabel('Optimal k')
    ax.set_title('Optimal k in the hyperplane')
    plt.show()


# hyperplane of
def prob_learning_hyperplane_plot(ev1=10, ev2=10, k_range=(1, 16)):
    ev1 = ev1
    ev2 = ev2
    k_values = np.arange(k_range[0], k_range[1])
    p_learn_values = np.linspace(0, 1, 20)  # Adjust the number of points as needed.
    k_grid, p_learn_grid = np.meshgrid(k_values, p_learn_values)

    pi_values = np.zeros_like(k_grid)

    for i in range(len(k_values)):
        for j in range(len(p_learn_values)):
            k = k_values[i]
            p_learn = p_learn_values[j]
            _, _, pi = monte_carlo(ev1_i=ev1, ev2_i=ev2, k=k, p_learn=p_learn)
            pi_values[j, i] = pi

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(k_grid, p_learn_grid, pi_values, cmap='viridis')
    ax.set_xlabel('k')
    ax.set_ylabel('p_learn')
    ax.set_zlabel('Auction House Profit (pi)')
    ax.set_title('Hyperplane with Fixed ev1 and ev2')
    plt.show()
