// Property investment calculator client in TypeScript (no backend required)
type LanguageCode = "en" | "de" | "zh";
type SummaryFormat = "currency" | "percent";
type SummaryConfigItem = {
  key: string;
  label: keyof typeof i18n["en"];
  format: SummaryFormat;
};
type FurnitureCategory = "kitchen" | "appliances" | "furniture";
type FurnitureItem = {
  name: string;
  category: FurnitureCategory;
  value: number;
};
type FurnitureItemsMap = Record<string, [number, number]>;
type PlotlyData = {
  x: number[];
  y: number[];
  mode: string;
  name: string;
};
type PlotlyLayout = {
  title: string;
  xaxis: { title: string };
  yaxis: { title: string };
  legend: { title: string };
  template: string;
  paper_bgcolor?: string;
  plot_bgcolor?: string;
  font?: { color?: string };
};
type PlotlyFigure = { data: PlotlyData[]; layout: PlotlyLayout };
type InvestmentResult = { figure: PlotlyFigure; summary: Record<string, number | null> };
type I18nDictionary = Record<string, string>;
type PropertyInvestmentParams = {
  purchase_price: number;
  mortgage_rate: number;
  loan_percentage: number;
  rental_income_monthly: number;
  hausgeld_monthly: number;
  grundsteuer_yearly: number;
  maintenance_reserve_per_sqm_yearly: number;
  apartment_size_sqm: number;
  principal_repayment_rate?: number;
  salary_income?: number;
  monthly_expenses?: number;
  salary_increase_rate?: number;
  years?: number;
  vacancy_rate?: number;
  property_transfer_tax_rate?: number;
  provision_rate?: number;
  notary_fee_rate?: number;
  grundbuch_fee_rate?: number;
  renovation_costs?: number;
  depreciation_rate?: number;
  land_value_per_sqm?: number;
  rental_increase_rate?: number;
  savings_interest_rate?: number;
  furniture_items?: FurnitureItemsMap | null;
  furniture_depreciation_method?: string;
  inflation_rates?: number[] | null;
  appreciation_rates?: number[] | null;
};

declare const Plotly: {
  react: (id: string, data: PlotlyData[], layout: PlotlyLayout, config?: Record<string, unknown>) => void;
};

const i18n: Record<LanguageCode, I18nDictionary> = {
  en: {
    appTitle: "🏠 Property Investment Calculator",
    appSubtitle: "Plan scenarios, compare outcomes, and understand cashflow implications.",
    lightMode: "Light",
    darkMode: "Dark",
    introHeading: "Scenario-based property analysis",
    introBody:
      "This simulation calculates the financial performance of a property investment over a specified period. It takes into account purchase price, mortgage rate, rental income, and expenses.",
    disclaimer: "Results are illustrative only and do not constitute personalized tax advice.",
    adLabel: "Advertisement",
    adPlaceholder: "Ad placeholder",
    inputHeading: "Input details",
    personalInfo: "👤 Personal Info",
    salaryIncome: "Salary Income (€/year)",
    monthlyExpenses: "Monthly Expenses (€)",
    salaryIncrease: "Salary Increase Rate (%)",
    savingsInterest: "Savings Interest Rate (%)",
    apartmentDetails: "🏢 Apartment Details",
    purchasePrice: "Purchase Price (€)",
    apartmentSize: "Apartment Size (sqm)",
    landValue: "Land Value per sqm (€)",
    hausgeld: "Hausgeld Monthly (€)",
    grundsteuer: "Grundsteuer Yearly (€)",
    maintenanceReserve: "Maintenance Reserve (€/sqm/year)",
    renovationCosts: "Renovation Costs (€)",
    rentalInfo: "🔑 Rental Information",
    rentalIncome: "Rental Income Monthly (€)",
    vacancyRate: "Vacancy Rate (%)",
    rentalIncrease: "Rental Increase Rate (%)",
    financeHeading: "Financing",
    purchaseCosts: "💰 Purchase Costs",
    transferTax: "Property Transfer Tax Rate (%)",
    provisionRate: "Provision Rate (%)",
    notaryFee: "Notary Fee Rate (%)",
    grundbuchFee: "Grundbuch Fee Rate (%)",
    mortgageValues: "🏦 Mortgage Values",
    mortgageRate: "Mortgage Rate (%)",
    loanPercentage: "Loan Percentage (%)",
    principalRepayment: "Principal Repayment Rate (%)",
    otherSettings: "⚙️ Other Settings",
    simulationYears: "Simulation Years",
    depreciationRate: "Property Depreciation Rate (%)",
    furnishingUnfurnished: "Unfurnished",
    furnishingFurnished: "Furnished (with depreciation)",
    furnitureHeading: "🪑 Furniture Depreciation",
    depreciationMethod: "Depreciation Method",
    methodBerlin: "Berlin Method (2% linear)",
    methodHamburg: "Hamburg Method (15% declining + 12% interest)",
    lifespanHeading: "Lifespan by Category",
    lifespanKitchen: "Kitchen (years)",
    lifespanAppliances: "Appliances (years)",
    lifespanFurniture: "Furniture (years)",
    furnitureItemsHeading: "Furniture Items",
    furnitureItem: "Item Name",
    furnitureCategory: "Category",
    furnitureValue: "Value (€)",
    addRow: "Add Row",
    calculateFurniture: "Calculate Furniture Depreciation",
    totalCost: "Total Cost",
    yearlyDepreciation: "Yearly Depreciation",
    simulationHeading: "📊 Simulation Output",
    simulationSubtitle: "Run the simulation to see how your property investment compares over time.",
    runSimulation: "Run Simulation",
    summaryHeading: "Summary Statistics",
    footerDisclaimer:
      "Results are illustrative only and should not be considered personalized financial or tax advice.",
    summaryLoanBalance: "Loan Balance after final year",
    summaryPropertyValue: "Property Value after final year",
    summaryPurchaseCosts: "Total Purchase Costs",
    summaryInitialInvestment: "Total Initial Investment",
    summaryAnnualDepreciation: "Annual Depreciation",
    summaryMonthlyPayment: "Minimum Monthly Loan Payment",
    summaryExpensesWith: "Total Expenses with Property",
    summaryExpensesWithout: "Total Expenses without Property",
    summaryRentalIncome: "Final Annual Rental Income",
    summaryTaxWith: "Tax Paid With Property (Last Year)",
    summaryTaxWithout: "Tax Paid Without Property (Last Year)",
    summaryNetWealthWith: "Final Net Wealth With Property",
    summaryNetWealthWithout: "Final Net Wealth Without Property",
    summaryWealthDelta: "Wealth Delta (With - Without)",
    summaryRoi: "ROI",
    summaryIrr: "IRR",
    categoryKitchen: "Kitchen",
    categoryAppliances: "Appliances",
    categoryFurniture: "Furniture",
  },
  de: {
    appTitle: "🏠 Immobilien-Investitionsrechner",
    appSubtitle: "Szenarien planen, Ergebnisse vergleichen und Cashflow verstehen.",
    lightMode: "Hell",
    darkMode: "Dunkel",
    introHeading: "Szenariobasierte Immobilienanalyse",
    introBody:
      "Diese Simulation berechnet die finanzielle Performance einer Immobilieninvestition über einen Zeitraum. Sie berücksichtigt Kaufpreis, Hypothekenzins, Mieteinnahmen und Ausgaben.",
    disclaimer: "Ergebnisse sind illustrativ und keine individuelle Steuerberatung.",
    adLabel: "Anzeige",
    adPlaceholder: "Platzhalter für Anzeige",
    inputHeading: "Eingaben",
    personalInfo: "👤 Persönliche Daten",
    salaryIncome: "Gehalt (€/Jahr)",
    monthlyExpenses: "Monatliche Ausgaben (€)",
    salaryIncrease: "Gehaltssteigerung (%)",
    savingsInterest: "Zins auf Ersparnisse (%)",
    apartmentDetails: "🏢 Wohnungsdetails",
    purchasePrice: "Kaufpreis (€)",
    apartmentSize: "Wohnfläche (qm)",
    landValue: "Bodenwert pro qm (€)",
    hausgeld: "Hausgeld monatlich (€)",
    grundsteuer: "Grundsteuer jährlich (€)",
    maintenanceReserve: "Instandhaltungsrücklage (€/qm/Jahr)",
    renovationCosts: "Renovierungskosten (€)",
    rentalInfo: "🔑 Mietinformationen",
    rentalIncome: "Mieteinnahmen monatlich (€)",
    vacancyRate: "Leerstandsquote (%)",
    rentalIncrease: "Mieterhöhung (%)",
    financeHeading: "Finanzierung",
    purchaseCosts: "💰 Kaufnebenkosten",
    transferTax: "Grunderwerbsteuer (%)",
    provisionRate: "Provision (%)",
    notaryFee: "Notargebühr (%)",
    grundbuchFee: "Grundbuchgebühr (%)",
    mortgageValues: "🏦 Hypothek",
    mortgageRate: "Hypothekenzins (%)",
    loanPercentage: "Finanzierungsanteil (%)",
    principalRepayment: "Tilgungsrate (%)",
    otherSettings: "⚙️ Weitere Einstellungen",
    simulationYears: "Simulationsjahre",
    depreciationRate: "Abschreibung (%)",
    furnishingUnfurnished: "Unmöbliert",
    furnishingFurnished: "Möbliert (mit Abschreibung)",
    furnitureHeading: "🪑 Möbelabschreibung",
    depreciationMethod: "Abschreibungsmethode",
    methodBerlin: "Berliner Methode (2% linear)",
    methodHamburg: "Hamburger Methode (15% degressiv + 12% Zins)",
    lifespanHeading: "Nutzungsdauer nach Kategorie",
    lifespanKitchen: "Küche (Jahre)",
    lifespanAppliances: "Geräte (Jahre)",
    lifespanFurniture: "Möbel (Jahre)",
    furnitureItemsHeading: "Möbelstücke",
    furnitureItem: "Bezeichnung",
    furnitureCategory: "Kategorie",
    furnitureValue: "Wert (€)",
    addRow: "Zeile hinzufügen",
    calculateFurniture: "Möbelabschreibung berechnen",
    totalCost: "Gesamtkosten",
    yearlyDepreciation: "Jährliche Abschreibung",
    simulationHeading: "📊 Simulationsergebnis",
    simulationSubtitle: "Simulation starten, um den Verlauf der Investition zu sehen.",
    runSimulation: "Simulation starten",
    summaryHeading: "Zusammenfassung",
    footerDisclaimer:
      "Ergebnisse sind illustrativ und ersetzen keine individuelle Finanz- oder Steuerberatung.",
    summaryLoanBalance: "Restschuld nach dem letzten Jahr",
    summaryPropertyValue: "Immobilienwert nach dem letzten Jahr",
    summaryPurchaseCosts: "Kaufnebenkosten gesamt",
    summaryInitialInvestment: "Gesamte Anfangsinvestition",
    summaryAnnualDepreciation: "Jährliche Abschreibung",
    summaryMonthlyPayment: "Minimale monatliche Kreditrate",
    summaryExpensesWith: "Gesamtausgaben mit Immobilie",
    summaryExpensesWithout: "Gesamtausgaben ohne Immobilie",
    summaryRentalIncome: "Mieteinnahmen im letzten Jahr",
    summaryTaxWith: "Steuern mit Immobilie (letztes Jahr)",
    summaryTaxWithout: "Steuern ohne Immobilie (letztes Jahr)",
    summaryNetWealthWith: "Vermögen mit Immobilie",
    summaryNetWealthWithout: "Vermögen ohne Immobilie",
    summaryWealthDelta: "Vermögensdifferenz (mit - ohne)",
    summaryRoi: "ROI",
    summaryIrr: "IRR",
    categoryKitchen: "Küche",
    categoryAppliances: "Geräte",
    categoryFurniture: "Möbel",
  },
  zh: {
    appTitle: "🏠 德国房产投资计算器",
    appSubtitle: "规划情景、对比结果并了解现金流影响。",
    lightMode: "浅色",
    darkMode: "深色",
    introHeading: "基于情景的房产分析",
    introBody:
      "该模拟计算在指定周期内房产投资的财务表现，涵盖购房价格、贷款利率、租金收入与费用。",
    disclaimer: "结果仅供参考，不构成个性化税务建议。",
    adLabel: "广告",
    adPlaceholder: "广告位占位",
    inputHeading: "输入信息",
    personalInfo: "👤 个人信息",
    salaryIncome: "年薪收入 (€/年)",
    monthlyExpenses: "每月支出 (€)",
    salaryIncrease: "工资增长率 (%)",
    savingsInterest: "储蓄利率 (%)",
    apartmentDetails: "🏢 公寓信息",
    purchasePrice: "购入价格 (€)",
    apartmentSize: "面积 (平方米)",
    landValue: "土地单价 (€ / 平方米)",
    hausgeld: "每月物业费 (€)",
    grundsteuer: "年度房产税 (€)",
    maintenanceReserve: "维护储备金 (€/平方米/年)",
    renovationCosts: "翻新费用 (€)",
    rentalInfo: "🔑 租赁信息",
    rentalIncome: "每月租金收入 (€)",
    vacancyRate: "空置率 (%)",
    rentalIncrease: "租金增长率 (%)",
    financeHeading: "融资",
    purchaseCosts: "💰 购房成本",
    transferTax: "房产交易税率 (%)",
    provisionRate: "中介费率 (%)",
    notaryFee: "公证费率 (%)",
    grundbuchFee: "土地登记费率 (%)",
    mortgageValues: "🏦 抵押贷款",
    mortgageRate: "贷款利率 (%)",
    loanPercentage: "贷款比例 (%)",
    principalRepayment: "本金偿还率 (%)",
    otherSettings: "⚙️ 其他设置",
    simulationYears: "模拟年限",
    depreciationRate: "房产折旧率 (%)",
    furnishingUnfurnished: "未家具",
    furnishingFurnished: "家具齐全（含折旧）",
    furnitureHeading: "🪑 家具折旧",
    depreciationMethod: "折旧方法",
    methodBerlin: "柏林方法（2% 直线）",
    methodHamburg: "汉堡方法（15% 递减 + 12% 利息）",
    lifespanHeading: "按类别的使用年限",
    lifespanKitchen: "厨房（年）",
    lifespanAppliances: "电器（年）",
    lifespanFurniture: "家具（年）",
    furnitureItemsHeading: "家具清单",
    furnitureItem: "物品名称",
    furnitureCategory: "类别",
    furnitureValue: "价值 (€)",
    addRow: "添加行",
    calculateFurniture: "计算家具折旧",
    totalCost: "总成本",
    yearlyDepreciation: "年折旧",
    simulationHeading: "📊 模拟输出",
    simulationSubtitle: "运行模拟以查看投资表现。",
    runSimulation: "运行模拟",
    summaryHeading: "汇总统计",
    footerDisclaimer: "结果仅供参考，不应视为个性化财务或税务建议。",
    summaryLoanBalance: "最终年度贷款余额",
    summaryPropertyValue: "最终年度房产价值",
    summaryPurchaseCosts: "总购房成本",
    summaryInitialInvestment: "初始总投资",
    summaryAnnualDepreciation: "年度折旧",
    summaryMonthlyPayment: "最低月供",
    summaryExpensesWith: "含房产的总支出",
    summaryExpensesWithout: "不含房产的总支出",
    summaryRentalIncome: "最终年度租金收入",
    summaryTaxWith: "含房产税负（最后一年）",
    summaryTaxWithout: "不含房产税负（最后一年）",
    summaryNetWealthWith: "含房产最终净资产",
    summaryNetWealthWithout: "不含房产最终净资产",
    summaryWealthDelta: "净资产差值（含-不含）",
    summaryRoi: "ROI",
    summaryIrr: "IRR",
    categoryKitchen: "厨房",
    categoryAppliances: "电器",
    categoryFurniture: "家具",
  },
};

const summaryConfig: SummaryConfigItem[] = [
  { key: "Loan Balance After Final Year", label: "summaryLoanBalance", format: "currency" },
  { key: "Property Value", label: "summaryPropertyValue", format: "currency" },
  { key: "Total Purchase Costs", label: "summaryPurchaseCosts", format: "currency" },
  { key: "Total Initial Investment", label: "summaryInitialInvestment", format: "currency" },
  { key: "Annual Depreciation", label: "summaryAnnualDepreciation", format: "currency" },
  { key: "Monthly Loan Payment (Annuität)", label: "summaryMonthlyPayment", format: "currency" },
  { key: "Total Expenses with Property", label: "summaryExpensesWith", format: "currency" },
  { key: "Total Expenses Without Property", label: "summaryExpensesWithout", format: "currency" },
  { key: "Operating Cashflow (Last Year)", label: "summaryRentalIncome", format: "currency" },
  { key: "Tax Paid With Property (Last Year)", label: "summaryTaxWith", format: "currency" },
  { key: "Tax Paid Without Property (Last Year)", label: "summaryTaxWithout", format: "currency" },
  { key: "Net Wealth With Property", label: "summaryNetWealthWith", format: "currency" },
  { key: "Net Wealth Without Property", label: "summaryNetWealthWithout", format: "currency" },
  { key: "Wealth Delta", label: "summaryWealthDelta", format: "currency" },
  { key: "ROI", label: "summaryRoi", format: "percent" },
  { key: "IRR", label: "summaryIrr", format: "percent" },
];

const defaultFurniture: FurnitureItem[] = [
  { name: "Built-in Kitchen", category: "kitchen", value: 5000 },
  { name: "Sofa", category: "furniture", value: 1000 },
];

const languageSelect = document.getElementById("languageSelect") as HTMLSelectElement;
const rangeInputs = document.querySelectorAll("input[type=range]") as NodeListOf<HTMLInputElement>;
const furnitureTableBody = document.querySelector("#furniture_table tbody") as HTMLTableSectionElement;
const addRowButton = document.getElementById("add_furniture_row") as HTMLButtonElement;
const calculateFurnitureButton = document.getElementById("calculate_furniture") as HTMLButtonElement;
const runSimulationButton = document.getElementById("run_simulation") as HTMLButtonElement;

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function randomNormal(mean = 0, stdDev = 1): number {
  let u = 0;
  let v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  const standardNormal = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  return mean + stdDev * standardNormal;
}

function randomUniform(min: number, max: number): number {
  return min + Math.random() * (max - min);
}

function getLocale(): string {
  if (languageSelect?.value === "de") return "de-DE";
  if (languageSelect?.value === "zh") return "zh-CN";
  return "en-US";
}

function calculateIRR(
  cashFlows: number[],
  guess = 0.1,
  iterations = 100,
  tolerance = 1e-6
): number | null {
  let rate = guess;
  for (let i = 0; i < iterations; i += 1) {
    let npv = 0;
    let derivative = 0;
    cashFlows.forEach((cf, t) => {
      const discount = (1 + rate) ** t;
      npv += cf / discount;
      derivative -= (t * cf) / discount / (1 + rate);
    });
    if (Math.abs(derivative) < 1e-12) break;
    const newRate = rate - npv / derivative;
    if (Math.abs(newRate - rate) < tolerance) {
      rate = newRate;
      break;
    }
    rate = newRate;
  }
  return Number.isFinite(rate) ? rate : null;
}

function estimateIncomeTax(grossIncome: number): { tax: number; net: number } {
  const allowance = 11604;
  let taxable = Math.max(0, grossIncome - allowance);
  let tax = 0;
  const brackets = [
    { upTo: 17700, rate: 0.14 },
    { upTo: 66760, rate: 0.3 },
    { upTo: 277825, rate: 0.42 },
    { upTo: Infinity, rate: 0.45 },
  ];
  let lastCap = 0;
  for (const bracket of brackets) {
    const portion = Math.max(0, Math.min(taxable, bracket.upTo - lastCap));
    tax += portion * bracket.rate;
    taxable -= portion;
    lastCap = bracket.upTo;
    if (taxable <= 0) break;
  }
  const net = grossIncome - tax;
  return { tax, net };
}

function calculateFurnitureDepreciation({
  method = "berlin",
  items = {},
  year = 1,
  hamburg_interest_rate = 0.12,
  hamburg_depreciation_rate = 0.15,
  hamburg_depreciation_years = 7,
}: {
  method?: string;
  items?: FurnitureItemsMap;
  year?: number;
  hamburg_interest_rate?: number;
  hamburg_depreciation_rate?: number;
  hamburg_depreciation_years?: number;
}): number {
  const entries = Object.values(items || {});
  if (!entries.length) return 0;
  return entries.reduce((total, [value, lifespan]) => {
    if (method === "berlin") {
      return total + value / lifespan;
    }
    const effectiveYear = Math.max(year, 1);
    const depreciatingValue =
      effectiveYear > hamburg_depreciation_years
        ? value * 0.3
        : value * (1 - hamburg_depreciation_rate) ** (effectiveYear - 1);
    const depreciation = depreciatingValue * hamburg_depreciation_rate;
    const capitalInterest = depreciatingValue * hamburg_interest_rate;
    return total + depreciation + capitalInterest;
  }, 0);
}

function buildFurnitureItems(items: FurnitureItem[], lifespans: Record<string, number>): FurnitureItemsMap {
  const lifespanMap = {
    kitchen: Math.max(1, Number(lifespans.kitchen ?? 10)),
    appliances: Math.max(1, Number(lifespans.appliances ?? 5)),
    furniture: Math.max(1, Number(lifespans.furniture ?? 10)),
  };

  return items.reduce<FurnitureItemsMap>((acc, item) => {
    const name = String(item.name || "").trim();
    const value = item.value;
    const category = (item.category as FurnitureCategory) || "furniture";
    if (name && Number.isFinite(value)) {
      const lifespan = lifespanMap[category] ?? 1;
      acc[name] = [Number(value), Number(lifespan)];
    }
    return acc;
  }, {});
}

function calculateLoanTermForMonthlyPayment(
  loanAmount: number,
  annualInterestRate: number,
  maxYears = 30
): [number, number] {
  const r = annualInterestRate / 12;
  const n = Math.floor(maxYears * 12);
  const monthlyPayment = loanAmount * ((r * (1 + r) ** n) / ((1 + r) ** n - 1));
  return [monthlyPayment, n];
}

function propertyInvestmentCalculator({
  purchase_price,
  mortgage_rate,
  loan_percentage,
  rental_income_monthly,
  hausgeld_monthly,
  grundsteuer_yearly,
  maintenance_reserve_per_sqm_yearly,
  apartment_size_sqm,
  principal_repayment_rate = 0.02,
  salary_income = 60000,
  monthly_expenses = 2000,
  salary_increase_rate = 0.02,
  years = 10,
  vacancy_rate = 0.05,
  property_transfer_tax_rate = 0.06,
  provision_rate = 0.0357,
  notary_fee_rate = 0.015,
  grundbuch_fee_rate = 0.005,
  renovation_costs = 0,
  depreciation_rate = 0.02,
  land_value_per_sqm = 0,
  rental_increase_rate = 0.02,
  savings_interest_rate = 0.02,
  furniture_items = null,
  furniture_depreciation_method = "berlin",
  inflation_rates = null,
  appreciation_rates = null,
}: PropertyInvestmentParams): InvestmentResult {
  const totalYears = Math.max(1, Math.floor(Number(years) || 0));

  const property_transfer_tax = purchase_price * property_transfer_tax_rate;
  const provision = purchase_price * provision_rate;
  const notary_fee = purchase_price * notary_fee_rate;
  const grundbuch_fee = purchase_price * grundbuch_fee_rate;

  const loan_amount = purchase_price * loan_percentage;

  let monthly_loan_payment: number;
  if (principal_repayment_rate > 0) {
    monthly_loan_payment = (loan_amount * (mortgage_rate + principal_repayment_rate)) / 12;
  } else {
    monthly_loan_payment = calculateLoanTermForMonthlyPayment(loan_amount, mortgage_rate)[0];
  }

  const total_furniture_costs = furniture_items
    ? Object.values(furniture_items).reduce((sum, [value]) => sum + value, 0)
    : 0;

  const total_purchase_costs = property_transfer_tax + provision + notary_fee + grundbuch_fee;

  const total_initial_investment =
    purchase_price + total_purchase_costs + total_furniture_costs + (renovation_costs as number);

  const maintenance_reserve_yearly = maintenance_reserve_per_sqm_yearly * apartment_size_sqm;

  const land_value = land_value_per_sqm * apartment_size_sqm;
  const building_value = purchase_price + (renovation_costs as number) - land_value;
  const depreciation_per_year = building_value * depreciation_rate;

  const yearly_hausgeld = hausgeld_monthly * 12;
  const yearly_loan_payment = monthly_loan_payment * 12;

  let balance = loan_amount;
  const loan_balances: number[] = [];
  const property_values: number[] = [];
  const total_expenses_over_years_with: number[] = [];
  const total_expenses_over_years_without: number[] = [];
  const tax_over_years_with: number[] = [];
  const tax_over_years_without: number[] = [];
  const rental_incomes: number[] = [];
  const operating_cashflows: number[] = [];
  let property_value = purchase_price;
  let annual_rental_income = rental_income_monthly * 12 * (1 - vacancy_rate);
  let cumulative_expenses_with = 0;
  let net_wealth_without = 0;
  let total_interest_paid = 0;
  const net_wealth_over_years_with: number[] = [];
  const net_wealth_over_years_without: number[] = [];
  const years_list: number[] = [];

  const initial_investment_with_furniture =
    purchase_price * (1 - loan_percentage) +
    purchase_price *
      (property_transfer_tax_rate + provision_rate + notary_fee_rate + grundbuch_fee_rate) +
    (renovation_costs as number) +
    total_furniture_costs;

  const cash_flows: number[] = [-initial_investment_with_furniture];

  let total_depreciation = depreciation_per_year;

  for (let year = 1; year <= totalYears; year += 1) {
    years_list.push(year);

    const interest_paid = balance * mortgage_rate;
    const principal_paid = yearly_loan_payment - interest_paid;
    balance = Math.max(balance - principal_paid, 0);
    total_interest_paid += interest_paid;
    loan_balances.push(balance);
    rental_incomes.push(annual_rental_income);

    const inflation =
      Array.isArray(inflation_rates) && inflation_rates.length >= year
        ? (inflation_rates[year - 1] as number)
        : randomNormal(0.02, 0.01);
    const random_inflation_rate = clamp(inflation, -0.02, 0.03);

    const inflated_hausgeld = yearly_hausgeld * (1 + random_inflation_rate) ** (year - 1);
    const inflated_grundsteuer = grundsteuer_yearly * (1 + random_inflation_rate) ** (year - 1);
    const inflated_maintenance_reserve =
      maintenance_reserve_yearly * (1 + random_inflation_rate) ** (year - 1);

    const operating_cashflow =
      annual_rental_income - inflated_hausgeld - inflated_grundsteuer - inflated_maintenance_reserve;
    operating_cashflows.push(operating_cashflow);

    const salary_now =
      salary_income * (1 + salary_increase_rate) ** year * (1 + random_inflation_rate);

    const furniture_depr = furniture_items
      ? calculateFurnitureDepreciation({
          method: furniture_depreciation_method as string,
          items: furniture_items as FurnitureItemsMap,
          year,
        })
      : 0;

    total_depreciation = depreciation_per_year + furniture_depr;

    const taxable_rental_income =
      annual_rental_income -
      interest_paid -
      total_depreciation -
      yearly_hausgeld -
      grundsteuer_yearly -
      maintenance_reserve_yearly;

    const taxResult = estimateIncomeTax(salary_now);
    const tax_salary = taxResult.tax;
    const netto_salary = taxResult.net;
    tax_over_years_without.push(tax_salary);
    const tax_rate = salary_now > 0 ? (tax_salary / salary_now) * 100 : 0;

    const tax_rental_income = taxable_rental_income * (tax_rate / 100);
    tax_over_years_with.push(tax_rental_income);
    const after_tax_salary_with = taxable_rental_income - tax_rental_income + netto_salary;

    const net_cash =
      operating_cashflows[operating_cashflows.length - 1] - yearly_loan_payment + tax_rental_income;
    cash_flows.push(net_cash);

    const after_tax_salary_without = salary_now - netto_salary;

    const living_expenses_yearly = monthly_expenses * 12 * (1 + random_inflation_rate);

    let investment_expenses_yearly =
      yearly_loan_payment + yearly_hausgeld + grundsteuer_yearly + maintenance_reserve_yearly;
    if (year === 1) {
      investment_expenses_yearly += total_purchase_costs;
    }

    const total_expense_for_year_with = investment_expenses_yearly + living_expenses_yearly;

    cumulative_expenses_with += total_expense_for_year_with;
    total_expenses_over_years_without.push(living_expenses_yearly);
    total_expenses_over_years_with.push(cumulative_expenses_with);

    const appreciation =
      Array.isArray(appreciation_rates) && appreciation_rates.length >= year
        ? (appreciation_rates[year - 1] as number)
        : randomUniform(-0.01, 0.07);
    property_value *= 1 + appreciation;
    property_values.push(property_value);

    const net_wealth_with = property_value - balance + after_tax_salary_with - monthly_expenses * 12;
    net_wealth_over_years_with.push(net_wealth_with);

    net_wealth_without += after_tax_salary_without - monthly_expenses * 12;
    net_wealth_over_years_without.push(net_wealth_without);

    annual_rental_income *= 1 + rental_increase_rate + random_inflation_rate;

    net_wealth_without *= (1 + savings_interest_rate) / (1 + random_inflation_rate || 1);
  }

  const total_rental_income = rental_incomes.reduce((sum, value) => sum + value, 0);
  const total_expenses =
    total_interest_paid +
    hausgeld_monthly * 12 * totalYears +
    grundsteuer_yearly * totalYears +
    maintenance_reserve_per_sqm_yearly * apartment_size_sqm * totalYears +
    (renovation_costs as number);

  const latest_balance = loan_balances[loan_balances.length - 1] ?? balance;
  const latest_property_value = property_values[property_values.length - 1] ?? property_value;
  const net_profit = latest_property_value - latest_balance + total_rental_income - total_expenses;

  const initial_investment =
    purchase_price * (1 - loan_percentage) +
    purchase_price *
      (property_transfer_tax_rate + provision_rate + notary_fee_rate + grundbuch_fee_rate) +
    (renovation_costs as number);

  const roi = initial_investment ? net_profit / initial_investment : 0;

  const final_resale_gain = latest_property_value - latest_balance;
  if (cash_flows.length) {
    cash_flows[cash_flows.length - 1] += final_resale_gain;
  } else {
    cash_flows.push(final_resale_gain);
  }
  const irr = calculateIRR(cash_flows);
  const irr_percent = irr !== null && isFinite(irr) ? irr * 100 : null;

  const figure: PlotlyFigure = {
    data: [
      {
        x: years_list,
        y: loan_balances,
        mode: "lines+markers",
        name: "Loan Balance",
      },
      {
        x: years_list,
        y: property_values,
        mode: "lines+markers",
        name: "Property Value",
      },
      {
        x: years_list,
        y: total_expenses_over_years_with,
        mode: "lines+markers",
        name: "Total Expenses With Property",
      },
      {
        x: years_list,
        y: total_expenses_over_years_without,
        mode: "lines+markers",
        name: "Total Expenses Without Property",
      },
      {
        x: years_list,
        y: years_list.map(() => depreciation_per_year),
        mode: "lines+markers",
        name: "Annual Depreciation",
      },
      {
        x: years_list,
        y: rental_incomes,
        mode: "lines+markers",
        name: "Annual Rental Income",
      },
      {
        x: years_list,
        y: operating_cashflows,
        mode: "lines+markers",
        name: "Operating Cashflow",
      },
      {
        x: years_list,
        y: tax_over_years_with,
        mode: "lines+markers",
        name: "Tax With Apartment",
      },
      {
        x: years_list,
        y: tax_over_years_without,
        mode: "lines+markers",
        name: "Tax Without Apartment",
      },
      {
        x: years_list,
        y: net_wealth_over_years_with,
        mode: "lines+markers",
        name: "Net Wealth With Property",
      },
      {
        x: years_list,
        y: net_wealth_over_years_without,
        mode: "lines+markers",
        name: "Net Wealth Without Property",
      },
    ],
    layout: {
      title: "Property Investment Overview",
      xaxis: { title: "Year" },
      yaxis: { title: "Amount (€)" },
      legend: { title: "Metrics" },
      template: "plotly_white",
    },
  };

  return {
    figure,
    summary: {
      "Loan Amount": loan_amount,
      "Monthly Loan Payment (Annuität)": monthly_loan_payment,
      "Total Purchase Costs": total_purchase_costs,
      "Total Initial Investment": total_initial_investment,
      "Annual Depreciation": total_depreciation,
      "Total Expenses with Property": total_expenses_over_years_with.slice(-1)[0] ?? 0,
      "Total Expenses Without Property": total_expenses_over_years_without.slice(-1)[0] ?? 0,
      "Loan Balance": latest_balance,
      "Property Value": latest_property_value,
      "Net Wealth With Property": net_wealth_over_years_with.slice(-1)[0] ?? 0,
      "Net Wealth Without Property": net_wealth_over_years_without.slice(-1)[0] ?? 0,
      "Operating Cashflow (Last Year)": operating_cashflows.slice(-1)[0] ?? 0,
      "Tax Paid With Property (Last Year)": tax_over_years_with.slice(-1)[0] ?? 0,
      "Tax Paid Without Property (Last Year)": tax_over_years_without.slice(-1)[0] ?? 0,
      "Loan Balance After Final Year": latest_balance,
      ROI: roi,
      IRR: irr_percent,
    },
  };
}

function setTheme(theme: string): void {
  document.documentElement.setAttribute("data-theme", theme);
  document.body.setAttribute("data-bs-theme", theme);
  localStorage.setItem("theme", theme);
}

function setLanguage(lang: LanguageCode): void {
  document.documentElement.lang = lang;
  const dictionary = i18n[lang] || i18n.en;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.getAttribute("data-i18n");
    if (key && dictionary[key]) {
      element.textContent = dictionary[key];
    }
  });
  updateFurnitureCategoryLabels(lang);
  updateSummaryLabels(lang);
}

function updateRangeValue(input: HTMLInputElement): void {
  const display = document.querySelector<HTMLElement>(`[data-range-value-for="${input.id}"]`);
  if (display) {
    display.textContent = `${input.value}%`;
  }
}

function createFurnitureRow(item: FurnitureItem = { name: "", category: "kitchen", value: 0 }): void {
  const row = document.createElement("tr");

  const nameCell = document.createElement("td");
  const nameInput = document.createElement("input");
  nameInput.type = "text";
  nameInput.className = "form-control form-control-sm";
  nameInput.value = item.name;
  nameCell.appendChild(nameInput);

  const categoryCell = document.createElement("td");
  const categorySelect = document.createElement("select");
  categorySelect.className = "form-select form-select-sm";
  categorySelect.innerHTML = `
    <option value="kitchen">${i18n[languageSelect.value as LanguageCode].categoryKitchen}</option>
    <option value="appliances">${i18n[languageSelect.value as LanguageCode].categoryAppliances}</option>
    <option value="furniture">${i18n[languageSelect.value as LanguageCode].categoryFurniture}</option>
  `;
  categorySelect.value = item.category;
  categoryCell.appendChild(categorySelect);

  const valueCell = document.createElement("td");
  const valueInput = document.createElement("input");
  valueInput.type = "number";
  valueInput.className = "form-control form-control-sm";
  valueInput.value = item.value.toString();
  valueCell.appendChild(valueInput);

  const deleteCell = document.createElement("td");
  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.className = "btn btn-outline-danger btn-sm";
  deleteButton.textContent = "×";
  deleteButton.addEventListener("click", () => row.remove());
  deleteCell.appendChild(deleteButton);

  row.append(nameCell, categoryCell, valueCell, deleteCell);
  furnitureTableBody.appendChild(row);
}

function updateFurnitureCategoryLabels(lang: LanguageCode): void {
  furnitureTableBody.querySelectorAll("select").forEach((select) => {
    const value = (select as HTMLSelectElement).value;
    (select as HTMLSelectElement).innerHTML = `
      <option value="kitchen">${i18n[lang].categoryKitchen}</option>
      <option value="appliances">${i18n[lang].categoryAppliances}</option>
      <option value="furniture">${i18n[lang].categoryFurniture}</option>
    `;
    (select as HTMLSelectElement).value = value;
  });
}

function collectFurnitureItems(): FurnitureItem[] {
  const rows = furnitureTableBody.querySelectorAll("tr");
  return Array.from(rows).map((row) => {
    const [nameInput, categorySelect, valueInput] = row.querySelectorAll("input, select") as NodeListOf<
      HTMLInputElement | HTMLSelectElement
    >;
    return {
      name: (nameInput as HTMLInputElement).value,
      category: (categorySelect as HTMLSelectElement).value as FurnitureCategory,
      value: Number((valueInput as HTMLInputElement).value || 0),
    };
  });
}

function getFormValue(id: string): string | number | boolean {
  const input = document.getElementById(id) as HTMLInputElement | null;
  if (!input) {
    return 0;
  }
  return input.type === "checkbox" ? input.checked : input.value;
}

function getFurnishingOption(): "unfurnished" | "furnished" {
  const selected = document.querySelector<HTMLInputElement>("input[name='furnishing_option']:checked");
  return selected ? (selected.value as "unfurnished" | "furnished") : "unfurnished";
}

function updateSummaryLabels(lang: LanguageCode): void {
  const list = document.getElementById("result_stats") as HTMLUListElement | null;
  if (!list) return;
  list.querySelectorAll("li").forEach((item) => {
    const labelKey = item.getAttribute("data-label-key") as keyof typeof i18n["en"];
    if (labelKey) {
      const labelSpan = item.querySelector("span");
      if (labelSpan) {
        labelSpan.textContent = i18n[lang][labelKey];
      }
    }
  });
}

function formatValue(value: number | null | undefined, format: SummaryFormat, locale = getLocale()): string {
  if (value === null || value === undefined) {
    return "-";
  }
  if (format === "percent") {
    return `${Number(value).toFixed(2)}%`;
  }
  if (format === "currency") {
    return new Intl.NumberFormat(locale, {
      style: "currency",
      currency: "EUR",
      maximumFractionDigits: 2,
    }).format(Number(value));
  }
  return String(value);
}

function renderSummary(summary: Record<string, number | null>): void {
  const list = document.getElementById("result_stats") as HTMLUListElement;
  list.innerHTML = "";
  const wealthDelta = (summary["Net Wealth With Property"] ?? 0) - (summary["Net Wealth Without Property"] ?? 0);
  const mergedSummary = { ...summary, "Wealth Delta": wealthDelta };

  summaryConfig.forEach((config) => {
    const listItem = document.createElement("li");
    listItem.className = "list-group-item d-flex justify-content-between align-items-start";
    listItem.setAttribute("data-label-key", config.label);

    const label = document.createElement("span");
    label.textContent = i18n[languageSelect.value as LanguageCode][config.label];
    const value = document.createElement("strong");
    value.textContent = formatValue(mergedSummary[config.key], config.format, getLocale());

    listItem.append(label, value);
    list.appendChild(listItem);
  });
}

function calculateFurniture(): void {
  const lifespans = {
    kitchen: Number(getFormValue("lifespan_kitchen")),
    appliances: Number(getFormValue("lifespan_appliances")),
    furniture: Number(getFormValue("lifespan_furniture")),
  };
  const furnitureItems = buildFurnitureItems(collectFurnitureItems(), lifespans);
  const depreciation = calculateFurnitureDepreciation({
    method: getFormValue("depreciation_method") as string,
    items: furnitureItems,
    year: 1,
  });
  const totalCost = Object.values(furnitureItems).reduce((sum, [value]) => sum + value, 0);

  const costNode = document.getElementById("furniture_cost");
  const depNode = document.getElementById("furniture_depreciation");
  if (costNode) costNode.textContent = formatValue(totalCost, "currency");
  if (depNode) depNode.textContent = formatValue(depreciation, "currency");
}

let lastFigure: PlotlyFigure | null = null;

function applyPlotlyTheme(figure: PlotlyFigure): PlotlyFigure {
  const theme = document.documentElement.getAttribute("data-theme") || "light";
  const layout: PlotlyLayout = { ...(figure.layout || {}) };
  if (theme === "dark") {
    layout.template = "plotly_dark";
    layout.paper_bgcolor = "rgba(0,0,0,0)";
    layout.plot_bgcolor = "rgba(0,0,0,0)";
    layout.font = { ...(layout.font || {}), color: "#f9fafb" };
  } else {
    layout.template = "plotly_white";
    layout.paper_bgcolor = "rgba(0,0,0,0)";
    layout.plot_bgcolor = "rgba(0,0,0,0)";
    layout.font = { ...(layout.font || {}), color: "#101828" };
  }
  return { ...figure, layout };
}

function runSimulation(): void {
  const furnishingOption = getFurnishingOption();
  const lifespans = {
    kitchen: Number(getFormValue("lifespan_kitchen")),
    appliances: Number(getFormValue("lifespan_appliances")),
    furniture: Number(getFormValue("lifespan_furniture")),
  };

  const furnitureItems =
    furnishingOption === "furnished" ? buildFurnitureItems(collectFurnitureItems(), lifespans) : null;

  const result = propertyInvestmentCalculator({
    purchase_price: Number(getFormValue("purchase_price")),
    mortgage_rate: Number(getFormValue("mortgage_rate")) / 100,
    loan_percentage: Number(getFormValue("loan_percentage")) / 100,
    rental_income_monthly: Number(getFormValue("rental_income_monthly")),
    hausgeld_monthly: Number(getFormValue("hausgeld_monthly")),
    grundsteuer_yearly: Number(getFormValue("grundsteuer_yearly")),
    maintenance_reserve_per_sqm_yearly: Number(getFormValue("maintenance_reserve_per_sqm_yearly")),
    apartment_size_sqm: Number(getFormValue("apartment_size_sqm")),
    principal_repayment_rate: Number(getFormValue("principal_repayment_rate")) / 100,
    salary_income: Number(getFormValue("salary_income")),
    monthly_expenses: Number(getFormValue("monthly_expenses")),
    salary_increase_rate: Number(getFormValue("salary_increase_rate")) / 100,
    years: Number(getFormValue("years")),
    vacancy_rate: Number(getFormValue("vacancy_rate")) / 100,
    property_transfer_tax_rate: Number(getFormValue("property_transfer_tax_rate")) / 100,
    provision_rate: Number(getFormValue("provision_rate")) / 100,
    notary_fee_rate: Number(getFormValue("notary_fee_rate")) / 100,
    grundbuch_fee_rate: Number(getFormValue("grundbuch_fee_rate")) / 100,
    renovation_costs: Number(getFormValue("renovation_costs")),
    depreciation_rate: Number(getFormValue("depreciation_rate")) / 100,
    land_value_per_sqm: Number(getFormValue("land_value_per_sqm")),
    rental_increase_rate: Number(getFormValue("rental_increase_rate")) / 100,
    savings_interest_rate: Number(getFormValue("savings_interest_rate")) / 100,
    furniture_items: furnitureItems,
    furniture_depreciation_method: getFormValue("depreciation_method") as string,
  });

  lastFigure = applyPlotlyTheme(result.figure);

  Plotly.react("investment_chart", lastFigure.data, lastFigure.layout, {
    responsive: true,
  });

  renderSummary(result.summary);
}

function init(): void {
  const savedTheme = (localStorage.getItem("theme") as string) || "light";
  setTheme(savedTheme);

  const savedLanguage = (localStorage.getItem("language") as LanguageCode) || "en";
  if (languageSelect) {
    languageSelect.value = savedLanguage;
  }
  setLanguage(savedLanguage);

  document.querySelectorAll<HTMLElement>("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const theme = button.getAttribute("data-theme-toggle");
      if (theme) {
        setTheme(theme);
        if (lastFigure) {
          const themedFigure = applyPlotlyTheme(lastFigure);
          Plotly.react("investment_chart", themedFigure.data, themedFigure.layout, {
            responsive: true,
          });
          lastFigure = themedFigure;
        }
      }
    });
  });

  languageSelect?.addEventListener("change", () => {
    const value = languageSelect.value as LanguageCode;
    localStorage.setItem("language", value);
    setLanguage(value);
  });

  rangeInputs.forEach((input) => {
    updateRangeValue(input);
    input.addEventListener("input", () => updateRangeValue(input));
  });

  defaultFurniture.forEach((item) => createFurnitureRow(item));

  addRowButton?.addEventListener("click", () => createFurnitureRow());
  calculateFurnitureButton?.addEventListener("click", calculateFurniture);
  runSimulationButton?.addEventListener("click", runSimulation);
}

init();
