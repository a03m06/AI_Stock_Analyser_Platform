import pandas as pd


# =====================================
# LOAD DATASETS
# =====================================

print("Loading NSE...")
nse = pd.read_csv(
    "database/companies/nse_companies.csv"
)

print("Loading NSE SME...")
sme = pd.read_csv(
    "database/companies/sme_companies.csv"
)

print("Loading BSE SME...")
bse = pd.read_csv(
    "database/companies/bse_companies.csv"
)


# =====================================
# MERGE
# =====================================

print("Merging datasets...")

all_companies = pd.concat(

    [
        nse,
        sme,
        bse
    ],

    ignore_index=True
)


# =====================================
# CLEAN
# =====================================

all_companies["company_name"] = (
    all_companies["company_name"]
    .astype(str)
    .str.strip()
)

all_companies["symbol"] = (
    all_companies["symbol"]
    .astype(str)
    .str.strip()
)

all_companies["industry"] = (
    all_companies["industry"]
    .fillna("")
)

all_companies["sector"] = (
    all_companies["sector"]
    .fillna("")
)


# remove duplicate companies

all_companies = (
    all_companies
    .drop_duplicates(
        subset=["company_name"]
    )
    .reset_index(
        drop=True
    )
)


# =====================================
# SAVE
# =====================================

all_companies.to_csv(

    "database/companies/all_companies.csv",

    index=False
)


# =====================================
# SUMMARY
# =====================================

print()

print(
    "NSE      :",
    len(nse)
)

print(
    "NSE SME  :",
    len(sme)
)

print(
    "BSE SME  :",
    len(bse)
)

print(
    "TOTAL    :",
    len(all_companies)
)

print()

print(
    all_companies.head()
)