import numpy as np
import plotly.graph_objs as go

# Parameters
P = 350000            # Purchase price
D = 1 * P           # Down payment
M = P - D              # Mortgage amount
r_m = 0.05             # Annual mortgage interest rate
n = 30                 # Mortgage term in years
T = 30                # Years planning to stay
C_p = 0.01             # Annual maintenance cost (1% of property value)
T_p = 0.0125           # Annual property tax (1.25%)
G = 0.049               # Annual property appreciation
S = 0.06               # Selling cost (6%)
O = 0.07               # Opportunity cost/investment return
R = 1300               # Monthly rent
i = 0.05               # Annual rent increase

# Mortgage monthly payment
monthly_rate = r_m / 12
num_payments = n * 12
PMT = M * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

# Time horizon in years
years = np.arange(1, T + 1)

# Arrays to store cumulative values
buying_costs = []
renting_costs = []

for t in years:
    mortgage_paid = PMT * 12 * t
    maintenance = C_p * P * t
    taxes = T_p * P * t
    lost_investment = D * ((1 + O) ** t - 1)
    future_home_value = P * (1 + G) ** t
    net_selling_value = future_home_value * (1 - S)
    total_buying_cost = mortgage_paid + maintenance + taxes + lost_investment - (net_selling_value - (P - M))
    buying_costs.append(total_buying_cost)

    rent_cost = sum([12 * R * ((1 + i) ** k) for k in range(t)])
    invested_value = D * ((1 + O) ** t)
    for k in range(t):
        annual_savings = C_p * P
        invested_value += annual_savings * ((1 + O) ** (t - k))
    total_renting_cost = rent_cost - invested_value
    renting_costs.append(total_renting_cost)

# Plotting
fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=buying_costs, mode='lines+markers', name='Buying Cost'))
fig.add_trace(go.Scatter(x=years, y=renting_costs, mode='lines+markers', name='Renting Cost'))
fig.update_layout(
    title='Buy vs Rent Cost Over Time',
    xaxis_title='Years',
    yaxis_title='Net Cost (USD)',
    legend_title='Option',
    template='plotly_white'
)
fig.show()