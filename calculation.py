import math
import random
from typing import Optional, Union

from lst2024 import Lohnsteuer2024
from lst2025 import Lohnsteuer2025
import plotly.graph_objects as go


def estimate_tax(income) -> Lohnsteuer2024:
    l = Lohnsteuer2024()
    l.setRe4(income)  # Cent
    l.setStkl(3)  # Tax class
    l.setLzz(1)  # Wage payment period, 2 = month
    l.setZkf(0)  # Kinder
    l.setPkv(0)  # GKV (default)
    l.setKvz(1.5)  # Health insurance contribution (1.50%)
    l.setKrv(0)  # RV-WEST (default)
    l.setAlter1(
        0
    )  # set 1 if the 64th year of life was completed at the beginning of the calendar year
    l.setAf(
        0
    )  # # 1 if the application of the factor procedure has been selected (only in tax class IV)
    l.setF(1)  # Factor
    l.setPvs(0)  # Only if in Saxony
    l.setR(0)  # Religion yes/no
    l.setLzzhinzu(0)  # Additional amount on the income tax card
    l.setPvz(0)  # 1, if surcharge for social long -term care insurance
    l.MAIN()
    return l


def property_investment_calculator(
    purchase_price,
    mortgage_rate,
    loan_percentage,
    rental_income_monthly,
    hausgeld_monthly,
    grundsteuer_yearly,
    maintenance_reserve_per_sqm_yearly,
    apartment_size_sqm,
    salary_income=60000,
    monthly_expenses=2000,
    salary_increase_rate=0.02,
    years=10,
    vacancy_rate=0.05,
    property_transfer_tax_rate=0.06,
    provision_rate=0.0357,
    notary_fee_rate=0.015,
    grundbuch_fee_rate=0.005,
    renovation_costs=0,
    depreciation_rate=0.02,
    land_value_per_sqm=0,
    rental_increase_rate=0.02,
    savings_interest_rate=0.02,
    furniture_items: Optional[Union[dict[str, float], dict[str, tuple]]] = None,
    furniture_depreciation_method: Optional[str] = "berlin",
) -> go.Figure:

    saved_args = {**locals()}  # Updated to make a copy per loco.loop
    print("Provided values are", saved_args)

    property_transfer_tax = purchase_price * property_transfer_tax_rate
    provision = purchase_price * provision_rate
    notary_fee = purchase_price * notary_fee_rate
    grundbuch_fee = purchase_price * grundbuch_fee_rate

    loan_amount = purchase_price * loan_percentage

    # Calculate the monthly loan payment using the annuity formula
    loan_period = calculate_loan_term_for_monthly_payment(
        loan_amount=loan_amount, annual_interest_rate=mortgage_rate
    )
    monthly_loan_payment = loan_period[0]  # Get the monthly payment from the tuple
    total_furniture_costs = 0.0
    if furniture_items:
        total_furniture_costs = sum([v[0] for v in furniture_items.values()])

    total_purchase_costs = (
        property_transfer_tax + provision + notary_fee + grundbuch_fee
    )

    total_initial_investment = (
        purchase_price + total_purchase_costs + total_furniture_costs + renovation_costs
    )

    maintenance_reserve_yearly = maintenance_reserve_per_sqm_yearly * apartment_size_sqm

    land_value = land_value_per_sqm * apartment_size_sqm
    building_value = purchase_price + renovation_costs - land_value
    depreciation_per_year = building_value * depreciation_rate

    yearly_hausgeld = hausgeld_monthly * 12
    yearly_loan_payment = monthly_loan_payment * 12

    balance = loan_amount
    loan_balances = []
    property_values = []
    total_expenses_over_years_with = []
    total_expenses_over_years_without = []

    taxable_incomes_with = []
    tax_over_years_with = []
    tax_over_years_without = []
    rental_incomes = []
    depreciation_over_year = []
    operating_cashflows = []
    property_value = purchase_price
    annual_rental_income = rental_income_monthly * 12 * (1 - vacancy_rate)
    cumulative_expenses_with = 0
    cumulative_expenses_without = 0
    net_wealth_without = 0
    net_wealth_over_years_with = []

    net_wealth_over_years_without = []

    for year in range(1, years + 1):
        # Calculate loan balance and annual rental income
        interest_paid = balance * mortgage_rate
        principal_paid = yearly_loan_payment - interest_paid
        balance -= principal_paid
        balance = max(balance, 0)
        loan_balances.append(balance)
        rental_incomes.append(annual_rental_income)
        # Generate a random inflation rate between -2% and +3% each year
        random_inflation_rate = max(-0.02, min(random.gauss(0.02, 0.01), 0.03))

        # Calculate operating cashflow
        operating_cashflow = (
            annual_rental_income
            - yearly_hausgeld
            - grundsteuer_yearly
            - maintenance_reserve_yearly
        )

        operating_cashflows.append(operating_cashflow)

        # Calculate salary with increase and inflation
        salary_now = (
            salary_income
            * (1 + salary_increase_rate) ** year
            * (1 + random_inflation_rate)
        )

        if furniture_items:
            # Add furniture depreciation to building depreciation
            furniture_depr = calculate_furniture_depreciation(
                method=furniture_depreciation_method, items=furniture_items, year=year
            )
        else:
            furniture_depr = 0.0
        total_depreciation = depreciation_per_year + furniture_depr

        # Calculate taxable income
        taxable_rental_income = (
            annual_rental_income
            - interest_paid
            - total_depreciation
            - yearly_hausgeld
            - grundsteuer_yearly
            - maintenance_reserve_yearly
        )
        taxable_incomes_with.append(taxable_rental_income)

        steur_salary = estimate_tax(salary_now * 100)
        netto_salary = float(steur_salary.getWvfrb()) / 100
        tax_salary = float((steur_salary.getLstlzz()) / 100)
        tax_over_years_without.append(tax_salary)
        tax_rate = tax_salary / salary_now * 100

        # Calculate tax with property
        tax_rental_income = taxable_rental_income * tax_rate / 100
        tax_over_years_with.append(tax_rental_income)
        after_tax_salary_with = (
            taxable_rental_income - tax_rental_income
        ) + netto_salary

        # Calculate Tax without property
        after_tax_salary_without = salary_now - netto_salary

        # Calculate expenses
        # Living expenses only
        living_expenses_yearly = monthly_expenses * 12 * (1 + random_inflation_rate)

        # Investment-related expenses
        investment_expenses_yearly = (
            yearly_loan_payment
            + yearly_hausgeld
            + grundsteuer_yearly
            + maintenance_reserve_yearly
        )
        if year == 1:
            investment_expenses_yearly += total_purchase_costs
        # Total expenses with property
        total_expense_for_year_with = (
            investment_expenses_yearly + living_expenses_yearly
        )
        cumulative_expenses_with += total_expense_for_year_with

        # Add expenses to the list
        cumulative_expenses_with += total_expense_for_year_with * (
            1 + random_inflation_rate
        )
        total_expenses_over_years_without.append(living_expenses_yearly)
        total_expenses_over_years_with.append(
            cumulative_expenses_with + living_expenses_yearly
        )

        # Property value appreciation and depreciation
        property_value *= 1 + random.uniform(-0.01, 0.07)  # Varying appreciation
        property_values.append(property_value)
        depreciation_over_year.append(total_depreciation)

        # Calculate net wealth with property
        net_wealth_with = (
            property_value - balance + after_tax_salary_with - (monthly_expenses * 12)
        )
        net_wealth_over_years_with.append(net_wealth_with)

        # Add this year's after-tax salary saving
        net_wealth_without += after_tax_salary_without - (monthly_expenses * 12)
        net_wealth_over_years_without.append(net_wealth_without)

        # Increment rent income for next year
        annual_rental_income *= 1 + rental_increase_rate + random_inflation_rate

        # Increment passive return for next year savings
        net_wealth_without *= (1 + savings_interest_rate) / (1 + random_inflation_rate)

    years_list = list(range(1, years + 1))

    print(f"Loan Balances after {years} years:  {loan_balances[-1]:.2f} €")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years_list, y=loan_balances, mode="lines+markers", name="Loan Balance"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list, y=property_values, mode="lines+markers", name="Property Value"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=total_expenses_over_years_with,
            mode="lines+markers",
            name="Total Expenses With Property",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=total_expenses_over_years_without,
            mode="lines+markers",
            name="Total Expenses Without Property",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=[depreciation_per_year for _ in years_list],
            mode="lines+markers",
            name="Annual Depreciation",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=rental_incomes,
            mode="lines+markers",
            name="Annual Rental Income",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=operating_cashflows,
            mode="lines+markers",
            name="Operating Cashflow",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=tax_over_years_with,
            mode="lines+markers",
            name="Tax With Apartment",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=tax_over_years_without,
            mode="lines+markers",
            name="Tax Without Apartment",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=net_wealth_over_years_with,
            mode="lines+markers",
            name="Net Wealth With Property",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_list,
            y=net_wealth_over_years_without,
            mode="lines+markers",
            name="Net Wealth Without Property",
        )
    )

    fig.update_layout(
        title="Property Investment Overview",
        xaxis_title="Year",
        yaxis_title="Amount (€)",
        legend_title="Metrics",
        template="plotly_white",
    )

    return {
        "figure": fig,
        "Loan Amount": loan_amount,
        "Monthly Loan Payment (Annuität)": monthly_loan_payment,
        "Total Purchase Costs": total_purchase_costs,
        "Total Initial Investment": total_initial_investment,
        "Annual Depreciation": total_depreciation,
        "Total Expenses with Property": total_expenses_over_years_with[-1],
        "Total Expenses Without Property": total_expenses_over_years_without[-1],
        "Loan Balance": loan_balances[-1] if loan_balances else 0,
        "Property Value": property_values[-1] if property_values else purchase_price,
        "Net Wealth With Property": (
            net_wealth_over_years_with[-1] if net_wealth_over_years_with else 0
        ),
        "Net Wealth Without Property": (
            net_wealth_over_years_without[-1] if net_wealth_over_years_without else 0
        ),
        "Operating Cashflow (Last Year)": (
            operating_cashflows[-1] if operating_cashflows else 0
        ),
        "Tax Paid With Property (Last Year)": (
            tax_over_years_with[-1] if tax_over_years_with else 0
        ),
        "Tax Paid Without Property (Last Year)": (
            tax_over_years_without[-1] if tax_over_years_without else 0
        ),
        "Loan Balance After Final Year": loan_balances[-1] if loan_balances else 0,
    }


def calculate_monthly_payment_from_term(
    loan_amount: float, annual_interest_rate: float, term_years: float
) -> float:
    """
    Calculate monthly loan payment for a given term and rate.
    """
    r = annual_interest_rate / 12
    n = int(term_years * 12)
    return loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def calculate_loan_term_for_monthly_payment(
    loan_amount: float,
    annual_interest_rate: float,
    max_years: int = 30,
    tolerance: float = 1e-2,
) -> tuple[float, float]:
    """
    Calculate the minimum monthly payment and the corresponding loan term (in months)
    to repay the loan within max_years.

    Returns a tuple of (minimum monthly payment, number of months).
    """
    r = annual_interest_rate / 12  # monthly interest rate
    n = max_years * 12
    monthly_payment = loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return monthly_payment, n


def calculate_furniture_depreciation(
    method: str = "berlin",
    items: dict = None,
    year: int = 1,
    hamburg_interest_rate: float = 0.12,
    hamburg_depreciation_rate: float = 0.15,
    hamburg_depreciation_years: int = 7,
) -> float:
    """
    Calculate total annual furniture depreciation using either Berlin or Hamburg method per item.

    Args:
        method: 'berlin' or 'hamburg'
        items: dict of furniture items with (value, useful_life) if berlin, or just value if hamburg
        year: which year of depreciation (1-indexed)
        hamburg_interest_rate: capital interest rate (Hamburg)
        hamburg_depreciation_rate: depreciation rate (Hamburg)
        hamburg_depreciation_years: depreciation duration (Hamburg)

    Returns:
        Total annual depreciation amount
    """
    if not items:
        return 0.0

    total = 0.0

    if method == "berlin":
        for _, (value, lifespan) in items.items():
            total += value / lifespan

    elif method == "hamburg":
        for _, (value, lifespan) in items.items():
            if year > hamburg_depreciation_years:
                current_value = value * 0.3
            else:
                current_value = value * ((1 - hamburg_depreciation_rate) ** (year - 1))
            depreciation = current_value * hamburg_depreciation_rate
            capital_interest = current_value * hamburg_interest_rate
            total += depreciation + capital_interest

    else:
        raise ValueError("Unknown depreciation method: choose 'berlin' or 'hamburg'")

    return total


def simulate_furnished_rental(
    base_rent: float,
    rent_uplift: float,
    vacancy_rate: float,
    tax_rate: float,
    furniture_items: dict,
    depreciation_method: str = "berlin",
    years: int = 10,
) -> float:
    """
    Simulates total net income for furnished rentals with depreciation.

    Args:
        base_rent: Monthly base rent (unfurnished)
        rent_uplift: % increase due to furnishing (e.g., 0.25 = 25%)
        vacancy_rate: Expected vacancy rate
        tax_rate: Effective tax rate
        furniture_items: Dict of furniture {name: value} or {name: (value, lifespan)}
        depreciation_method: 'berlin' or 'hamburg'
        years: Simulation duration

    Returns:
        Total net income after tax (over years)
    """
    gross_rent_yearly = base_rent * (1 + rent_uplift) * 12 * (1 - vacancy_rate)
    net_income = 0.0
    for year in range(1, years + 1):
        income = gross_rent_yearly
        depreciation = calculate_furniture_depreciation(
            method=depreciation_method, items=furniture_items, year=year
        )
        taxable = income - depreciation
        tax = max(taxable, 0) * tax_rate
        net_income += income - tax
    return net_income


example_result = property_investment_calculator(
    purchase_price=300000,
    mortgage_rate=0.04,
    loan_percentage=1,
    rental_income_monthly=1200,
    hausgeld_monthly=300,
    grundsteuer_yearly=400,
    maintenance_reserve_per_sqm_yearly=0,
    apartment_size_sqm=60,
    salary_income=6400 * 12,
    savings_interest_rate=0,
    vacancy_rate=0.02,
    years=32,
    renovation_costs=15000,
    depreciation_rate=0.02,
    land_value_per_sqm=1100,
)


"""
for key, value in example_result.items():
    if isinstance(value, list):
        print(f"{key}: {value}")
    else:
        print(f"{key}: {value:.2f} €")
"""

print(
    calculate_loan_term_for_monthly_payment(
        loan_amount=300000, annual_interest_rate=0.04
    )
)
