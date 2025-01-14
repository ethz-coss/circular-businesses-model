import matplotlib.pyplot as plt
import numpy as np
import models.monopoly.model as monopoly
import models.competition.model as competition
import models.spatial.model as spatial
import models.spatial_zones.model as spatial_zones
from parameters import NUM_CONSUMERS, NUM_COMPANIES
from utils import compare_solutions
import math

def get_mean_and_std(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    return mean, std

# Number of runs
n_runs = 5 # Number of runs
n_steps = 170 # 70  # Number of time steps

# Initialize data storage
n_companies = NUM_COMPANIES
money_data = np.zeros((n_runs, n_steps, n_companies))
prices_data = np.zeros((n_runs, n_steps, n_companies))
quantities_data = np.zeros((n_runs, n_steps, n_companies))
sold_data = np.zeros((n_runs, n_steps, n_companies))

waste_data = np.zeros((n_runs, n_steps, n_companies))
resources_left_data = np.zeros((n_runs, n_steps, n_companies))
material_pool_data = np.zeros((n_runs, n_steps, n_companies))
total_material_purchased_data = np.zeros((n_runs, n_steps, n_companies))

resources_costs_data = np.zeros((n_runs, n_steps, n_companies))
production_costs_data = np.zeros((n_runs, n_steps, n_companies))
maintenance_costs_data = np.zeros((n_runs, n_steps, n_companies))
avg_cost_per_product_data = np.zeros((n_runs, n_steps, n_companies))

# Run the model multiple times
for run in range(n_runs):

    print(f"Run {run+1}/{n_runs}")

    # model = monopoly.CircularEconomyModel(n=NUM_CONSUMERS)
    # model = competition.CircularEconomyModel(n=NUM_CONSUMERS)
    # model = spatial.CircularEconomyModel(n=NUM_CONSUMERS)
    model = spatial_zones.CircularEconomyModel(n=NUM_CONSUMERS)

    for step in range(n_steps):

        print(f"Step {step+1}/{n_steps} of run {run+1}/{n_runs}")

        model.step()
        model_data = model.datacollector.get_model_vars_dataframe()

        money_data[run, step, :] = model_data["Profits"].iloc[step]
        prices_data[run, step, :] = model_data["Prices"].iloc[step]
        quantities_data[run, step, :] = model_data["Quantities"].iloc[step]
        sold_data[run, step, :] = model_data["Amount Sold"].iloc[step]

        waste_data[run, step, :] = model_data["Waste"].iloc[step]
        resources_left_data[run, step, :] = model_data["Remaining Resources"].iloc[step]
        material_pool_data[run, step, :] = model_data["Material Pools"].iloc[step]
        total_material_purchased_data[run, step, :] = model_data["Total Material Purchased"].iloc[step]

        resources_costs_data[run, step, :] = model_data["Resource Costs"].iloc[step]
        production_costs_data[run, step, :] = model_data["Production Costs"].iloc[step]
        maintenance_costs_data[run, step, :] = model_data["Maintenance Costs"].iloc[step]
        avg_cost_per_product_data[run, step, :] = model_data["Avg Cost Per Product"].iloc[step]

    # all_price_differences_sol1 = []
    # all_price_differences_sol2 = []
    # all_quantity_differences_sol1 = []
    # all_quantity_differences_sol2 = []
    # all_profit_differences_sol1 = []
    # all_profit_differences_sol2 = []

    # for company in model.companies:
    #     print(f"Company Circularity: {company.circularity}")

    #     # Price Comparison
    #     price_differences_sol1 = compare_solutions(company.sol3_prices, company.sol1_prices)
    #     price_differences_sol2 = compare_solutions(company.sol3_prices, company.sol2_prices)
    #     all_price_differences_sol1.extend(price_differences_sol1)
    #     all_price_differences_sol2.extend(price_differences_sol2)

    #     # Quantity Comparison
    #     quantity_differences_sol1 = compare_solutions(company.sol3_quants, company.sol1_quants)
    #     quantity_differences_sol2 = compare_solutions(company.sol3_quants, company.sol2_quants)
    #     all_quantity_differences_sol1.extend(quantity_differences_sol1)
    #     all_quantity_differences_sol2.extend(quantity_differences_sol2)

    #     # Profit Comparison
    #     profit_differences_sol1 = compare_solutions(company.sol3_profits, company.sol1_profits)
    #     profit_differences_sol2 = compare_solutions(company.sol3_profits, company.sol2_profits)
    #     all_profit_differences_sol1.extend(profit_differences_sol1)
    #     all_profit_differences_sol2.extend(profit_differences_sol2)

    # # now print mean and std of the differences
    # print("Price Differences Solution 1")
    # print(np.mean(all_price_differences_sol1), np.std(all_price_differences_sol1))
    # print("Price Differences Solution 2")
    # print(np.mean(all_price_differences_sol2), np.std(all_price_differences_sol2))
    
    # print("Quantity Differences Solution 1")
    # print(np.mean(all_quantity_differences_sol1), np.std(all_quantity_differences_sol1))
    # print("Quantity Differences Solution 2")
    # print(np.mean(all_quantity_differences_sol2), np.std(all_quantity_differences_sol2))

    # print("Profit Differences Solution 1")
    # print(np.mean(all_profit_differences_sol1), np.std(all_profit_differences_sol1))
    # print("Profit Differences Solution 2")
    # print(np.mean(all_profit_differences_sol2), np.std(all_profit_differences_sol2))

# Calculate mean and std for each company
time_steps = range(n_steps)

money_mean, money_std = get_mean_and_std(money_data)
prices_mean, prices_std = get_mean_and_std(prices_data)
quantities_mean, quantities_std = get_mean_and_std(quantities_data)
sold_mean, sold_std = get_mean_and_std(sold_data)

waste_mean, waste_std = get_mean_and_std(waste_data)
resources_mean, resources_std = get_mean_and_std(resources_left_data)
materials_mean, materials_std = get_mean_and_std(material_pool_data)
total_material_purchased_mean, total_material_purchased_std = get_mean_and_std(total_material_purchased_data)

resources_costs_mean, resources_costs_std = get_mean_and_std(resources_costs_data)
production_costs_mean, production_costs_std = get_mean_and_std(production_costs_data)
maintenance_costs_mean, maintenance_costs_std = get_mean_and_std(maintenance_costs_data)
avg_cost_per_product_mean, avg_cost_per_product_std = get_mean_and_std(avg_cost_per_product_data)

# Colors for companies
colors = ["blue", "orange", "green", "red", "purple"]

# Create subplots
fig, axs = plt.subplots(2, 3, figsize=(15, 18))

# Plot each production with mean and std
def plot_with_std(ax, mean, std, title, ylabel):
    for i in range(n_companies):
        ax.plot(time_steps, mean[:, i], label=f"Circularity {model.companies[i].circularity:.1f}", color=model.companies[i].color)
        ax.fill_between(
            time_steps,
            mean[:, i] - std[:, i],
            mean[:, i] + std[:, i],
            color=model.companies[i].color,
            alpha=0.2
        )
    ax.set_title(title)
    ax.set_xlabel("Time Step")
    ax.set_ylabel(ylabel)
    # ax.legend()

def plot_with_std_zones(ax, mean, std, title, ylabel):
    colors = ["green", "blue", "purple", "orange"]
    for i in range(n_companies):
        j = math.floor(i / 2)
        ax.plot(time_steps, mean[:, i], label=f"Zone {j+1}", color=colors[j])
        ax.fill_between(
            time_steps,
            mean[:, i] - std[:, i],
            mean[:, i] + std[:, i],
            color=model.companies[i].color,
            alpha=0.2
        )
    ax.set_title(title)
    ax.set_xlabel("Time Step")
    ax.set_ylabel(ylabel)
    ax.legend()

# Plot each production
# fig.suptitle("Circularity Subsidy (=200 * Circularity)", fontsize=16)
# fig.suptitle("Waste Penalty (=2 * Waste)", fontsize=16)
# fig.suptitle("Consumer Preferences more Eco-friendly", fontsize=16)
# fig.suptitle("Raw Material Tax (=1 * Raw Material Purchased)", fontsize=16)
# fig.suptitle("Limited Material Purchases", fontsize=16)
plot_with_std_zones(axs[0][0], money_mean, money_std, "Money Over Time", "Money")
# plot_with_std(axs[0][1], waste_mean, waste_std, "Waste Over Time", "Waste")
plot_with_std_zones(axs[0][1], prices_mean, prices_std, "Prices Over Time", "Price")
plot_with_std_zones(axs[0][2], sold_mean, sold_std, "Amount Sold Over Time", "Amount Sold")
# plot_with_std(axs[0][2], avg_cost_per_product_mean, avg_cost_per_product_std, "Average Cost Per Product Over Time", "Average Cost Per Product")

plot_with_std_zones(axs[1][0], quantities_mean, quantities_std, "Quantities Over Time", "Quantity")
plot_with_std_zones(axs[1][1], resources_mean, resources_std, "Remaining Resources Over Time", "Resources")
# plot_with_std(axs[1][1], sold_mean, sold_std, "Amount Sold Over Time", "Amount Sold")
plot_with_std_zones(axs[1][2], materials_mean, materials_std, "Material Pools Over Time", "Material Pool")

# plot_with_std(axs[1][0], resources_costs_mean, resources_costs_std, "Resource Costs Over Time", "Resource Costs")
# plot_with_std(axs[2][1], production_costs_mean, production_costs_std, "Production Costs Over Time", "Production Costs")
# plot_with_std(axs[2][2], maintenance_costs_mean, maintenance_costs_std, "Maintenance Costs Over Time", "Maintenance Costs")

# # Adjust layout
# plt.tight_layout()
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adds space at the top
plt.subplots_adjust(hspace=0.3, wspace=0.3)  # Adds vertical spacing between rows of subplots
plt.show()

# # Calculate total material purchased by each company
# total_material_purchased = np.sum(material_pool_data, axis=(0, 1))  # Sum over runs and steps

# # Create a bar plot
# company_labels = [f"Company {i+1}" for i in range(n_companies)]
# plt.figure(figsize=(10, 6))
# plt.bar(company_labels, total_material_purchased_mean[-1, :], color=colors)

# # Add titles and labels
# plt.title("Total Material Purchased by Each Company")
# plt.xlabel("Company")
# plt.ylabel("Total Material Purchased")

# # Show the plot
# plt.tight_layout()
# plt.show()


# # Calculate distances between companies
# from scipy.spatial import distance

# # Get positions of companies on the grid
# company_positions = [agent.pos for agent in model.companies]

# # Calculate distance to nearest other company
# nearest_distances = []
# for i, pos in enumerate(company_positions):
#     other_positions = company_positions[:i] + company_positions[i+1:]
#     dists = distance.cdist([pos], other_positions, metric='euclidean')
#     nearest_distances.append(np.min(dists))

# # Extract profits at the end of the simulation
# final_profits = money_mean[-1, :]

# # Extract circularity colors for the companies
# circularity_colors = [colors[i % len(colors)] for i in range(n_companies)]

# from sklearn.linear_model import LinearRegression
# import numpy as np

# # Reshape data for fitting (scikit-learn expects 2D arrays)
# X = np.array(nearest_distances).reshape(-1, 1)
# y = np.array(final_profits)

# # Fit a linear regression model
# reg = LinearRegression()
# reg.fit(X, y)

# # Predict profits using the fitted model
# y_pred = reg.predict(X)

# # Plot profits against nearest distances with colors based on circularity
# plt.figure(figsize=(10, 6))
# for i in range(n_companies):
#     plt.scatter(
#         nearest_distances[i], 
#         final_profits[i], 
#         color=circularity_colors[i], 
#         label=f"Company {i+1} (Circularity {(i % 5) * 0.2:.1f})"
#     )

# # Plot the regression line
# plt.plot(nearest_distances, y_pred, color="black", linestyle="--", label="Fitted Line")

# # Add titles and labels
# plt.title("Profits vs. Distance to Nearest Company (Colored by Circularity)")
# plt.xlabel("Distance to Nearest Company")
# plt.ylabel("Profits")
# plt.grid(True)

# # # Avoid duplicate labels in legend
# # handles, labels = plt.gca().get_legend_handles_labels()
# # by_label = dict(zip(labels, handles))
# # plt.legend(by_label.values(), by_label.keys())

# plt.tight_layout()
# plt.show()

# # Print slope and intercept of the fitted line
# print(f"Slope: {reg.coef_[0]:.2f}, Intercept: {reg.intercept_:.2f}")




