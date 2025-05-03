import dash
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go

from calculation import calculate_furniture_depreciation, property_investment_calculator
from controls import create_input, create_slider

import dash_bootstrap_components as dbc

from settings import get_value, load_ui_state, persist_dict, persist_value

# external JavaScript files
external_scripts = []

# external CSS stylesheets
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
]

app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)


app.layout = html.Div(
    [
        html.H1("🏠 Property Investment Calculator", style={"textAlign": "center"}),
        html.P(
            "This simulation calculates the financial performance of a property investment over a specified period. "
            "It takes into account various factors such as purchase price, mortgage rate, rental income, and expenses."
        ),
        html.Div(
            [
                # Column 1
                html.Div(
                    [
                        html.H3("👤 Personal Info"),
                        create_input(
                            "Salary Income (€/year)", "salary_income", 6400 * 12
                        ),
                        create_slider(
                            "Salary Increase Rate (%)",
                            "salary_increase_rate",
                            0,
                            10,
                            0.1,
                            2,
                        ),
                        create_slider(
                            "Savings Interest Rate (%)",
                            "savings_interest_rate",
                            0,
                            10,
                            0.1,
                            0,
                        ),
                        create_input("Monthly Expenses (€)", "monthly_expenses", 2000),
                        html.H3("🏢 Apartment Details"),
                        create_input("Purchase Price (€)", "purchase_price", 300000),
                        create_input("Apartment Size (sqm)", "apartment_size_sqm", 60),
                        create_input(
                            "Land Value per sqm (€)", "land_value_per_sqm", 1100
                        ),
                        create_input("Hausgeld Monthly (€)", "hausgeld_monthly", 300),
                        create_input(
                            "Grundsteuer Yearly (€)", "grundsteuer_yearly", 400
                        ),
                        create_input(
                            "Maintenance Reserve (€/sqm/year)",
                            "maintenance_reserve_per_sqm_yearly",
                            0,
                        ),
                        create_input("Renovation Costs (€)", "renovation_costs", 5000),
                        html.H3("🔑 Rental Information"),
                        create_input(
                            "Rental Income Monthly (€)", "rental_income_monthly", 1500
                        ),
                        create_slider(
                            "Vacancy Rate (%)", "vacancy_rate", 0, 10, 0.1, 2
                        ),
                        create_slider(
                            "Rental Increase Rate (%)",
                            "rental_increase_rate",
                            0,
                            10,
                            0.1,
                            2,
                        ),
                    ],
                    style={
                        "width": "45%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "20px",
                    },
                ),
                # Column 2
                html.Div(
                    [
                        html.H3("💰 Purchase Costs"),
                        create_slider(
                            "Property Transfer Tax Rate (%)",
                            "property_transfer_tax_rate",
                            0,
                            10,
                            0.1,
                            6,
                        ),
                        create_slider(
                            "Provision Rate (%)", "provision_rate", 0, 10, 0.1, 3.57
                        ),
                        create_slider(
                            "Notary Fee Rate (%)", "notary_fee_rate", 0, 5, 0.1, 1.5
                        ),
                        create_slider(
                            "Grundbuch Fee Rate (%)",
                            "grundbuch_fee_rate",
                            0,
                            5,
                            0.1,
                            0.5,
                        ),
                        html.H3("🏦 Mortgage Values"),
                        create_slider(
                            "Mortgage Rate (%)", "mortgage_rate", 0, 10, 0.1, 4
                        ),
                        create_slider(
                            "Loan Percentage (%)", "loan_percentage", 0, 100, 1, 100
                        ),
                        create_slider(
                            "Principal Repayment Rate (%)",
                            "principal_repayment_rate",
                            0,
                            10,
                            0.1,
                            2,
                        ),
                        html.H3("⚙️ Other Settings"),
                        create_input("Simulation Years", "years", 32),
                        create_slider(
                            "Property Depreciation Rate (%)",
                            "depreciation_rate",
                            0,
                            10,
                            0.1,
                            2,
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "Furnishing Option",
                                    style={"display": "inline-block"},
                                ),
                                dcc.RadioItems(
                                    inline=True,
                                    labelStyle={
                                        "display": "inline-block",
                                        "margin-left": "20px",
                                    },
                                    id="furnishing_option",
                                    options=[
                                        {
                                            "label": "Unfurnished",
                                            "value": "unfurnished",
                                        },
                                        {
                                            "label": "Furnished (with depreciation)",
                                            "value": "furnished",
                                        },
                                    ],
                                    value="unfurnished",
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "width": "45%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "padding": "20px",
                    },
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.H2("🪑 Furniture Calculation", style={"textAlign": "center"}),
                dbc.Accordion(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "Depreciation Method",
                                    style={
                                        "display": "inline-block",
                                        "vertical-align": "top",
                                        "margin-left": "20px",
                                        "width": "20%",
                                    },
                                ),
                                html.Div(
                                    style={"display": "inline-block", "width": "5%"},
                                ),
                                dcc.Dropdown(
                                    id="depreciation_method",
                                    options=[
                                        {
                                            "label": "Berlin Method (2% linear)",
                                            "value": "berlin",
                                        },
                                        {
                                            "label": "Hamburg Method (15% declining + 12% interest)",
                                            "value": "hamburg",
                                        },
                                    ],
                                    value="berlin",
                                    style={"width": "70%", "display": "inline-block"},
                                    persistence="depreciation_method",
                                    persistence_type="local",
                                ),
                            ]
                        ),
                        dbc.AccordionItem(
                            [
                                html.H5("1️⃣ Define Lifespan by Category"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            create_input(
                                                "Kitchen (years)",
                                                "lifespan_kitchen",
                                                10,
                                            )
                                        ),
                                        dbc.Col(
                                            create_input(
                                                "Appliances (years)",
                                                "lifespan_appliances",
                                                5,
                                            )
                                        ),
                                        dbc.Col(
                                            create_input(
                                                "Furniture (years)",
                                                "lifespan_furniture",
                                                10,
                                            )
                                        ),
                                    ]
                                ),
                            ],
                            title="Furniture Categories",
                        ),
                        dbc.AccordionItem(
                            [
                                html.H5("2️⃣ Add Furniture Items"),
                                dash_table.DataTable(
                                    id="furniture_table",
                                    columns=[
                                        {
                                            "name": "Item Name",
                                            "id": "name",
                                            "presentation": "input",
                                        },
                                        {
                                            "name": "Category",
                                            "id": "category",
                                            "presentation": "dropdown",
                                        },
                                        {
                                            "name": "Value (€)",
                                            "id": "value",
                                            "presentation": "input",
                                        },
                                    ],
                                    editable=True,
                                    row_deletable=True,
                                    dropdown={
                                        "category": {
                                            "options": [
                                                {
                                                    "label": "Kitchen",
                                                    "value": "kitchen",
                                                },
                                                {
                                                    "label": "Appliances",
                                                    "value": "appliances",
                                                },
                                                {
                                                    "label": "Furniture",
                                                    "value": "furniture",
                                                },
                                            ],
                                            "className": "dropdown columns",
                                        },
                                    },
                                    data=get_value(
                                        "furniture_table",
                                        [
                                            {
                                                "name": "Built-in Kitchen",
                                                "category": "kitchen",
                                                "value": 5000,
                                            },
                                            {
                                                "name": "Sofa",
                                                "category": "furniture",
                                                "value": 1000,
                                            },
                                        ],
                                    ),
                                ),
                                html.Br(),
                                dbc.Button(
                                    "Add Row", id="add_furniture_row", n_clicks=0
                                ),
                            ],
                            title="Furniture Items",
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Calculate Furniture Depreciation",
                                    id="calculate_furniture_depreciation",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [
                                        html.H5(
                                            "3️⃣ Total Cost",
                                            style={
                                                "display": "inline-block",
                                                "margin": "20px",
                                            },
                                        ),
                                        html.Label(
                                            id="furniture_cost",
                                            children="Click Calculate",
                                            style={
                                                "display": "inline-block",
                                                "margin": "20px",
                                            },
                                        ),
                                        html.H5(
                                            "4️⃣ Yearly Depreciation",
                                            style={
                                                "display": "inline-block",
                                                "margin": "20px",
                                            },
                                        ),
                                        html.Label(
                                            id="furniture_depreciation",
                                            children="Click Calculate",
                                            style={
                                                "display": "inline-block",
                                                "margin": "20px",
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            style={"textAlign": "center", "margin": "20px"},
                        ),
                    ]
                ),
            ],
            style={
                "border": "2px black solid",
                "border-radius": "5px",
                "margin": "20px",
            },
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.Button(
                    "Run Simulation",
                    id="run_simulation",
                    n_clicks=0,
                    style={"width": "200px", "fontSize": "18px"},
                ),
            ],
            style={"textAlign": "center"},
        ),
        html.Br(),
        html.Br(),
        html.Div(
            children=[
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [html.Div(id="result_stats")], title="📊 Simulation Summary"
                        )
                    ]
                ),
                dcc.Graph(id="investment_graph"),
            ],
            style={
                "border": "2px black solid",
                "border-radius": "5px",
                "margin": "20px",
            },
        ),
    ]
)


@app.callback(
    Output("investment_graph", "figure"),
    Output("result_stats", "children"),
    Input("run_simulation", "n_clicks"),
    State("purchase_price", "value"),
    State("mortgage_rate", "value"),
    State("loan_percentage", "value"),
    State("principal_repayment_rate", "value"),
    State("rental_income_monthly", "value"),
    State("hausgeld_monthly", "value"),
    State("grundsteuer_yearly", "value"),
    State("maintenance_reserve_per_sqm_yearly", "value"),
    State("apartment_size_sqm", "value"),
    State("salary_income", "value"),
    State("monthly_expenses", "value"),
    State("salary_increase_rate", "value"),
    State("years", "value"),
    State("vacancy_rate", "value"),
    State("property_transfer_tax_rate", "value"),
    State("provision_rate", "value"),
    State("notary_fee_rate", "value"),
    State("grundbuch_fee_rate", "value"),
    State("renovation_costs", "value"),
    State("depreciation_rate", "value"),
    State("land_value_per_sqm", "value"),
    State("rental_increase_rate", "value"),
    State("savings_interest_rate", "value"),
    State("furnishing_option", "value"),
    State("furniture_table", "data"),
    State("depreciation_method", "value"),
    Input("lifespan_kitchen", "value"),
    Input("lifespan_appliances", "value"),
    Input("lifespan_furniture", "value"),
)
def run_simulation(
    n_clicks,
    purchase_price,
    mortgage_rate,
    loan_percentage,
    principal_repayment_rate,
    rental_income_monthly,
    hausgeld_monthly,
    grundsteuer_yearly,
    maintenance_reserve_per_sqm_yearly,
    apartment_size_sqm,
    salary_income,
    monthly_expenses,
    salary_increase_rate,
    years,
    vacancy_rate,
    property_transfer_tax_rate,
    provision_rate,
    notary_fee_rate,
    grundbuch_fee_rate,
    renovation_costs,
    depreciation_rate,
    land_value_per_sqm,
    rental_increase_rate,
    savings_interest_rate,
    funishing_option,
    furniture_table,
    depreciation_method,
    lifespan_kitchen,
    lifespan_appliances,
    lifespan_furniture,
):
    if n_clicks == 0:
        return go.Figure()

    saved_args = {**locals()}
    persist_dict(saved_args)  # Updated to make a copy per loco.loop

    if funishing_option == "furnished":
        # build the furniture data structure
        furniture_items = build_funiture_items(
            furniture_table,
            lifespan_kitchen=lifespan_kitchen,
            lifespan_appliances=lifespan_appliances,
            lifespan_furniture=lifespan_furniture,
        )

        # run property_investment_calculator(...)
        result = property_investment_calculator(
            purchase_price=purchase_price,
            mortgage_rate=mortgage_rate / 100,
            loan_percentage=loan_percentage / 100,
            rental_income_monthly=rental_income_monthly,
            hausgeld_monthly=hausgeld_monthly,
            grundsteuer_yearly=grundsteuer_yearly,
            maintenance_reserve_per_sqm_yearly=maintenance_reserve_per_sqm_yearly,
            apartment_size_sqm=apartment_size_sqm,
            salary_income=salary_income,
            monthly_expenses=monthly_expenses,
            salary_increase_rate=salary_increase_rate / 100,
            property_transfer_tax_rate=property_transfer_tax_rate / 100,
            provision_rate=provision_rate / 100,
            notary_fee_rate=notary_fee_rate / 100,
            grundbuch_fee_rate=grundbuch_fee_rate / 100,
            rental_increase_rate=rental_increase_rate / 100,
            vacancy_rate=vacancy_rate / 100,
            depreciation_rate=depreciation_rate / 100,
            savings_interest_rate=savings_interest_rate / 100,
            years=years,
            renovation_costs=renovation_costs,
            land_value_per_sqm=land_value_per_sqm,
            furniture_items=furniture_items,
            furniture_depreciation_method=depreciation_method,
        )
    else:
        # run property_investment_calculator(...)
        result = property_investment_calculator(
            purchase_price=purchase_price,
            mortgage_rate=mortgage_rate / 100,
            loan_percentage=loan_percentage / 100,
            rental_income_monthly=rental_income_monthly,
            hausgeld_monthly=hausgeld_monthly,
            grundsteuer_yearly=grundsteuer_yearly,
            maintenance_reserve_per_sqm_yearly=maintenance_reserve_per_sqm_yearly,
            apartment_size_sqm=apartment_size_sqm,
            salary_income=salary_income,
            monthly_expenses=monthly_expenses,
            salary_increase_rate=salary_increase_rate / 100,
            property_transfer_tax_rate=property_transfer_tax_rate / 100,
            provision_rate=provision_rate / 100,
            notary_fee_rate=notary_fee_rate / 100,
            grundbuch_fee_rate=grundbuch_fee_rate / 100,
            rental_increase_rate=rental_increase_rate / 100,
            vacancy_rate=vacancy_rate / 100,
            depreciation_rate=depreciation_rate / 100,
            savings_interest_rate=savings_interest_rate / 100,
            years=years,
            renovation_costs=renovation_costs,
            land_value_per_sqm=land_value_per_sqm,
        )

    # Grab values for summary
    summary_list = html.Ul(
        [
            html.Li(
                f"🏦 Loan Balance after {years} years: {result['Loan Balance After Final Year']:.2f} €"
            ),
            html.Li(
                f"🏠 Property Value after {years} years: {result['Property Value']:.2f} €"
            ),
            html.Li(f"💸 Total Purchase Costs: {result['Total Purchase Costs']:.2f} €"),
            html.Li(
                f"🧱 Total Initial Investment: {result['Total Initial Investment']:.2f} €"
            ),
            html.Li(f"📈 Annual Depreciation: {result['Annual Depreciation']:.2f} €"),
            html.Li(
                f"💼 Minimum Monthly Loan Payment: {result['Monthly Loan Payment (Annuität)']:.2f} €"
            ),
            html.Li(
                f"🧾 Total Expenses with Property: {result['Total Expenses with Property']:.2f} €"
            ),
            html.Li(
                f"💡 Total Expenses without Property: {result['Total Expenses Without Property']:.2f} €"
            ),
            html.Li(
                f"📊 Final Annual Rental Income: {result['Operating Cashflow (Last Year)']:.2f} €"
            ),
            html.Li(
                f"💶 Tax Paid With Property (Year {years}): {result['Tax Paid With Property (Last Year)']:.2f} €"
            ),
            html.Li(
                f"🧮 Tax Paid Without Property (Year {years}): {result['Tax Paid Without Property (Last Year)']:.2f} €"
            ),
            html.Li(
                f"📈 Final Net Wealth With Property: {result['Net Wealth With Property']:.2f} €"
            ),
            html.Li(
                f"📉 Final Net Wealth Without Property: {result['Net Wealth Without Property']:.2f} €"
            ),
            html.Li(
                f"📐 Wealth Delta (With - Without): {result['Net Wealth With Property'] - result['Net Wealth Without Property'] } €"
            ),
        ]
    )

    return result["figure"], html.Details(
        [html.Summary("📊 Expand Summary Statistics"), summary_list]
    )


@app.callback(
    Output("furniture_table", "data"),
    Input("add_furniture_row", "n_clicks"),
    State("furniture_table", "data"),
)
def add_furniture_row(n_clicks, data):
    if n_clicks > 0:
        persist_value("furniture_table", data)
        data.append({"name": "", "category": "kitchen", "value": 0})
    return data


@app.callback(
    Output("furniture_depreciation", "children"),
    Output("furniture_cost", "children"),
    Input("calculate_furniture_depreciation", "n_clicks"),
    Input("depreciation_method", "value"),
    Input("lifespan_kitchen", "value"),
    Input("lifespan_appliances", "value"),
    Input("lifespan_furniture", "value"),
    State("furniture_table", "data"),
)
def calculate_furniture(
    n_clicks,
    depreciation_method,
    lifespan_kitchen,
    lifespan_appliances,
    lifespan_furniture,
    furniture_table,
):
    if n_clicks > 0:
        # persist values to local file
        saved_args = {**locals()}
        persist_dict(saved_args)  # Updated to make a copy per loco.loop

        # build the furniture data structure
        items = build_funiture_items(
            furniture_table,
            lifespan_kitchen=lifespan_kitchen,
            lifespan_appliances=lifespan_appliances,
            lifespan_furniture=lifespan_furniture,
        )
        # calculate depreciation
        depreciation_value = calculate_furniture_depreciation(
            method=depreciation_method, items=items
        )
        return f"{depreciation_value} €", f"{sum([v[0] for v in items.values()])} €"
    return "Click Calculate", "Click Calculate"


def build_funiture_items(
    furniture_table, lifespan_kitchen, lifespan_appliances, lifespan_furniture
):
    items: dict[str, tuple[int | float, int]] = {}
    for item in furniture_table:
        if item["name"] and item["value"]:
            items[item["name"]] = (
                float(item["value"]),
                {
                    "kitchen": lifespan_kitchen,
                    "appliances": lifespan_appliances,
                    "furniture": lifespan_furniture,
                }[item["category"]],
            )
    return items


if __name__ == "__main__":
    app.server.run(debug=True)
