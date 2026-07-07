from financial_agent import get_financial_data

company = {
    "company_name": "Tata Consultancy Services Limited",
    "symbol": "TCS",
    "exchange": "NSE"
}

result = get_financial_data(company)

print(result)
print(
    result["historical_returns"]
)