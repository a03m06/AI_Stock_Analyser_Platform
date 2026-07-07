import pandas as pd

# read original BSE file
bse = pd.read_csv(
    "database/companies/bse_companies.csv"
)

# convert to common schema
bse_new = pd.DataFrame({

    "company_name":
    bse["Scrip Name"],

    "symbol":
    bse["Scrip ID"],

    "exchange":
    "BSE SME",

    "sector":
    bse["Industry"],

    "industry":
    bse["Industry"],

    "theme":
    "",

    "market_cap_type":
    "Micro",

    "is_sme":
    True
})

# save new file
bse_new.to_csv(
    "database/companies/bse_companies.csv",
    index=False
)

print(bse_new.head())
print()
print("TOTAL:", len(bse_new))