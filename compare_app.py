import random
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from calculation import property_investment_calculator, compare_properties
from controls import create_input, create_slider

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def property_inputs(prefix: str):
    return dbc.Card(
        [
            html.H5(f"🏠 Property {prefix[-1].upper()}", className="card-title"),
            html.H6("🏚️ Property Details"),
            html.Div(
                [
                    html.Div(
                        [
                            create_input(
                                "Purchase Price (€)", f"{prefix}_price", 300000
                            ),
                            create_input("Apartment Size (sqm)", f"{prefix}_size", 60),
                            create_input(
                                "Hausgeld Monthly (€)", f"{prefix}_hausgeld", 300
                            ),
                            create_input("Renovation Cost", f"{prefix}_renovation", 0),
                        ],
                        style={
                            "display": "inline-block",
                            "width": "45%",
                            "margin": "10px",
                        },
                    ),
                    html.Div(
                        [
                            create_input(
                                "Rental Income Monthly (€)", f"{prefix}_rent", 1200
                            ),
                            create_input(
                                "Grundsteuer Yearly (€)", f"{prefix}_tax", 400
                            ),
                            create_input(
                                "Land Value per sqm (€)", f"{prefix}_land_value", 1100
                            ),
                            create_input(
                                "Maintenance Reserve (€/sqm/year)",
                                f"{prefix}_maintenance_reserve",
                                0,
                            ),
                        ],
                        style={
                            "display": "inline-block",
                            "width": "45%",
                            "margin": "10px",
                        },
                    ),
                ]
            ),
            html.H6("💰 Purchase Costs"),
            html.Div(
                [
                    html.Div(
                        [
                            create_slider(
                                "Property Transfer Tax Rate (%)",
                                f"{prefix}_transfer_tax_rate",
                                0,
                                10,
                                0.1,
                                6,
                            ),
                            create_slider(
                                "Provision Rate (%)",
                                f"{prefix}_provision_rate",
                                0,
                                10,
                                0.1,
                                3.57,
                            ),
                        ],
                        style={"display": "inline-block", "width": "50%"},
                    ),
                    html.Div(
                        [
                            create_slider(
                                "Notary Fee Rate (%)",
                                f"{prefix}_notary_fee",
                                0,
                                5,
                                0.1,
                                1.5,
                            ),
                            create_slider(
                                "Grundbuch Fee Rate (%)",
                                f"{prefix}_grundbuch_fee",
                                0,
                                5,
                                0.1,
                                0.5,
                            ),
                        ],
                        style={"display": "inline-block", "width": "50%"},
                    ),
                ]
            ),
        ],
        body=True,
    )


def shared_inputs():
    return dbc.Card(
        [
            html.H5("📊 Shared Inputs", className="card-title"),
            create_input("Salary Income (€/year)", "salary", 6400 * 12),
            create_input("Monthly Expenses (€)", "expenses", 2000),
            create_input("Years", "years", 30),
            create_input("Mortgage Rate (%)", "rate", 4, 0.1),
            create_input("Loan Percentage (%)", "loan_pct", 100, 1),
        ],
        body=True,
    )


app.layout = dbc.Container(
    [
        html.H2("📈 Property Investment Comparison"),
        dbc.Row(
            [
                dbc.Col(property_inputs("a"), width=6),
                dbc.Col(property_inputs("b"), width=6),
            ]
        ),
        html.Hr(),
        shared_inputs(),
        html.Br(),
        dbc.Button(
            "Compare Properties",
            id="compare_btn",
            n_clicks=0,
            color="primary",
            style={"display": "block", "margin-left": "auto", "margin-right": "auto"},
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.Div(id="results_a"), width=6),
                dbc.Col(html.Div(id="results_b"), width=6),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("results_a", "children"),
    Output("results_b", "children"),
    Input("compare_btn", "n_clicks"),
    State("a_price", "value"),
    State("a_rent", "value"),
    State("a_size", "value"),
    State("a_hausgeld", "value"),
    State("a_tax", "value"),
    State("a_land_value", "value"),
    State("a_renovation", "value"),
    State("a_transfer_tax_rate", "value"),
    State("a_provision_rate", "value"),
    State("a_notary_fee", "value"),
    State("a_grundbuch_fee", "value"),
    State("b_price", "value"),
    State("b_rent", "value"),
    State("b_size", "value"),
    State("b_hausgeld", "value"),
    State("b_tax", "value"),
    State("b_land_value", "value"),
    State("b_renovation", "value"),
    State("b_transfer_tax_rate", "value"),
    State("b_provision_rate", "value"),
    State("b_notary_fee", "value"),
    State("b_grundbuch_fee", "value"),
    State("salary", "value"),
    State("expenses", "value"),
    State("years", "value"),
    State("rate", "value"),
    State("loan_pct", "value"),
    State("a_maintenance_reserve", "value"),
    State("b_maintenance_reserve", "value"),
)
def compare_props(
    n,
    a_price,
    a_rent,
    a_size,
    a_haus,
    a_tax,
    a_land,
    a_renovation,
    a_transfer_tax_rate,
    a_provision_rate,
    a_notary_fee,
    a_grundbuch_fee,
    b_price,
    b_rent,
    b_size,
    b_haus,
    b_tax,
    b_land,
    b_renovation,
    b_transfer_tax_rate,
    b_provision_rate,
    b_notary_fee,
    b_grundbuch_fee,
    salary,
    expenses,
    years,
    rate,
    loan_pct,
    a_maintenance_reserve,
    b_maintenance_reserve,
):
    if n == 0:
        return "", ""

    inflation_rates = [random.gauss(0.02, 0.01) for _ in range(years)]
    appreciation_rates = [random.uniform(-0.01, 0.07) for _ in range(years)]

    common = {
        "mortgage_rate": rate / 100,
        "loan_percentage": loan_pct / 100,
        "salary_income": salary,
        "monthly_expenses": expenses,
        "years": years,
        "inflation_rates": inflation_rates,
        "appreciation_rates": appreciation_rates,
    }

    params_a = {
        "purchase_price": a_price,
        "rental_income_monthly": a_rent,
        "apartment_size_sqm": a_size,
        "hausgeld_monthly": a_haus,
        "grundsteuer_yearly": a_tax,
        "land_value_per_sqm": a_land,
        "renovation_costs": a_renovation,
        "property_transfer_tax_rate": a_transfer_tax_rate / 100,
        "provision_rate": a_provision_rate / 100,
        "notary_fee_rate": a_notary_fee / 100,
        "grundbuch_fee_rate": a_grundbuch_fee / 100,
        "maintenance_reserve_per_sqm_yearly": a_maintenance_reserve,
        **common,
    }

    params_b = {
        "purchase_price": b_price,
        "rental_income_monthly": b_rent,
        "apartment_size_sqm": b_size,
        "hausgeld_monthly": b_haus,
        "grundsteuer_yearly": b_tax,
        "land_value_per_sqm": b_land,
        "renovation_costs": b_renovation,
        "property_transfer_tax_rate": b_transfer_tax_rate / 100,
        "provision_rate": b_provision_rate / 100,
        "notary_fee_rate": b_notary_fee / 100,
        "grundbuch_fee_rate": b_grundbuch_fee / 100,
        "maintenance_reserve_per_sqm_yearly": b_maintenance_reserve,
        **common,
    }

    result_a = property_investment_calculator(**params_a)
    result_b = property_investment_calculator(**params_b)

    def summary_card(label, result):
        welath_delta: float = (
            result["Net Wealth With Property"] - result["Net Wealth Without Property"]
        )
        total_investment: float = result["Total Initial Investment"]
        roi = welath_delta / total_investment * 100 if total_investment != 0 else 0

        return dbc.Card(
            [
                html.H5(label, className="card-title"),
                dcc.Graph(figure=result["figure"]),
                html.Ul(
                    [
                        html.Li(
                            f"Net Wealth: €{result['Net Wealth With Property']:.2f}"
                        ),
                        html.Li(f"Property Value: €{result['Property Value']:.2f}"),
                        html.Li(f"Loan Balance: €{result['Loan Balance']:.2f}"),
                        html.Li(
                            f"💼 Minimum Monthly Loan Payment: {result['Monthly Loan Payment (Annuität)']:.2f} €"
                        ),
                        html.Li(
                            f"Final Rental Income: €{result['Operating Cashflow (Last Year)']:.2f}"
                        ),
                        html.Li(
                            f"Tax Paid Last Year: €{result['Tax Paid With Property (Last Year)']:.2f}"
                        ),
                        html.Li(
                            f"📐 Wealth Delta (With - Without): {result['Net Wealth With Property'] - result['Net Wealth Without Property'] } €"
                        ),
                        html.Li(f"🌟 ROI: {result['ROI']}"),
                    ]
                ),
            ],
            body=True,
        )

    return summary_card("Property A", result_a), summary_card("Property B", result_b)


if __name__ == "__main__":
    app.run(debug=True)
