# %%
# model of training overhang over time
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import latex

# %%
cost = 1000
cost_per_flop_year = 0.8
flops_per_dollar_year0 = 1e9 / 0.02
alg_gains_train = 1.8
alg_gains = alg_gains_train

# Chinchilla function relating compute to perplexity
chin_func = lambda x: 1070 * x ** (-0.154) + 1.7
total_loss = lambda cost, time: chin_func(
    (alg_gains**time) * flops_per_dollar_year0 * cost / (cost_per_flop_year**time)
)

# %%
# Graph this function with respect to time
time = np.linspace(0, 100, 100)
player1_growth = 1.5
player2_growth = 1.1

# Loss for best model over time
player2loss = total_loss(1000 * (player2_growth) ** time, time)
player1loss = total_loss(1000 * (player1_growth) ** time, time)
logistic_investment = lambda time: 10000 / (1 + np.exp(-0.1 * (time - 10)))
logistic_loss = total_loss(logistic_investment(time), time)

# Graph with multiple costs adding cost labels
plt.figure(figsize=(10, 5))
for c in [1000, 10000, 100000]:
    loss = total_loss(c, time)
    plt.plot(time, player1loss, label="Exponential Investment")
    plt.plot(time, loss, label=f"Cost: {c}")
    plt.plot(time, logistic_loss, label="Logistic Investment")

plt.xlabel("Time (years)")
plt.ylabel("Total Loss")
plt.legend()
plt.title("Training Loss Over Time")
plt.grid(True)

# %%
# Plot of overhang over time
plt.figure(figsize=(10, 5))
plt.plot(
    time, player1loss / total_loss(1000, time), label="Overhang over constant player"
)
plt.plot(time, player1loss / player2loss, label="Second Best Model")
plt.plot(
    time,
    logistic_loss / total_loss(1000, time),
    label="Overhang over logistic investment",
)

plt.xlabel("Time (years)")
plt.ylabel("Perplexity Overhang")
plt.legend()
plt.title("Training Overhang Over Time")
plt.grid(True)

# %%
# Model of inference overhang with a set number of parameters
player1_growth = 1.9
player2_growth = 1.0
alg_gains_inf = 1.2

total_loss_inf = lambda cost, time: chin_func(
    (
        (cost / (cost_per_flop_year**time)) ** 2
        * (alg_gains_train**time)
        * flops_per_dollar_year0
    )
)

time = np.linspace(0, 40, 10000)
plt.figure(figsize=(10, 5))
for c in [1000, 10000, 100000]:
    loss = total_loss(c, time)
    plt.plot(time, loss, label=f"Cost: {c}")

best_loss_seq = total_loss(1 * (player1_growth) ** time, time)
inf_overhang = total_loss_inf(100000, time) / total_loss_inf(100, time)
inf_bestvs1000dollars = best_loss_seq / total_loss_inf(1, time)

plt.ylabel("Total Loss for Models")
plt.xlabel("Time (years)")
plt.title("Inference Overhang for Given Inference Cost")
plt.legend()
plt.grid(True)

plt.figure(figsize=(10, 5))
plt.plot(
    time,
    inf_overhang,
    "r",
    label="Inference Overhang 100000 dollar model vs 100 dollar model",
)
plt.plot(
    time,
    inf_bestvs1000dollars,
    label="Inference Overhang Best Model vs 1000 dollar model",
)

plt.title("Inference Overhang of 10000 dollar model vs 100 dollar model Over Time")
plt.xlabel("Time (years)")
plt.ylabel("Overhang of Inference")
plt.legend()
plt.grid(True)

# %%
# Plot inference overhang and training overhang at the same time
player1loss = total_loss(1000 * (player1_growth) ** time, time)
plt.figure(figsize=(10, 5))
plt.plot(time, player1loss/total_loss_inf(1, time), label="Inference Overhang")
plt.plot(time, player1loss / total_loss(1000, time), label="Training Overhang")

plt.xlabel("Time (years)")
plt.ylabel("Overhang")
plt.legend()
plt.title("Inference and Training Overhang Over Time")
plt.grid(True)

# %%
# Inference overhang for constant parameter models
time = np.linspace(0, 100, 10000)
cost_per_flop_year = 1
loss_constant = 1.7
const_params = 1
A = 1
loss_const_param = (
    lambda time: loss_constant + A / (const_params * alg_gains**time) ** 0.34
)

plt.figure(figsize=(10, 5))
plt.xlabel("Time (years)")
plt.ylabel("Inference Overhang")
world_loss_seq = total_loss(1000 * (player1_growth) ** time, time)
loss_infoptimal_year_seq = loss_const_param(time)
plt.plot(time, world_loss_seq / loss_infoptimal_year_seq, label="Inference Overhang")

plt.title("world_best/const_param Over Time")
plt.legend()
plt.grid(True)

# %%
# Another model of inference overhang assuming fixed parameters for better and base model
time = np.linspace(0, 40, 10000)
plt.figure(figsize=(10, 5))
plt.plot(time, 1.5 ** (-0.034 * time), label="Inference Overhang")

# %%
# Symbolic computations for overhang
# Define the variables
cost, time = sp.symbols("cost time")
g_alg, C0, I, t, g_flop, g_invest = sp.symbols("g_alg C0 I t g_flop g_invest")

# Define the function
chin_func = 1070 * I ** (-0.154) + 1.7
total_loss = chin_func.subs(I, (g_alg**t) * C0 * I * g_flop**t)

# Simplify and display the function
total_loss = sp.simplify(total_loss)
overhang = total_loss.subs(
    I, (g_alg**t) * g_invest**t * C0 * I * g_flop**t
) / total_loss.subs(I, C0 * I * (g_alg**t) * g_flop**t)
overhang = sp.simplify(overhang)

print(latex(total_loss))
sp.pprint(total_loss)
print("The overhang is")
sp.pprint(overhang)

# %%
