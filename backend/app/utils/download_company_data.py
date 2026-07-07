import os
import pandas as pd
import requests


# =====================================
# Create folders
# =====================================

os.makedirs(
    "database/companies",
    exist_ok=True
)


# =====================================
# NSE Companies
# =====================================

def download_nse():

    print("\nDownloading NSE companies...")

    url = (
        "https://archives.nseindia.com/"
        "content/equities/EQUITY_L.csv"
    )

    df = pd.read_csv(url)

    nse = pd.DataFrame()

    nse["company_name"] = df[
        "NAME OF COMPANY"
    ]

    nse["symbol"] = df[
        "SYMBOL"
    ]

    nse["exchange"] = "NSE"

    nse["sector"] = ""

    nse["industry"] = ""

    nse["theme"] = ""

    nse["market_cap_type"] = ""

    nse["is_sme"] = False

    nse.to_csv(

        "database/companies/nse_companies.csv",

        index=False
    )

    print(
        "NSE:",
        len(nse)
    )

    return nse


# =====================================
# BSE Companies
# =====================================

def download_bse():

    print(
        "\nDownloading BSE companies..."
    )

    url = (
        "https://api.bseindia.com/"
        "BseIndiaAPI/api/"
        "ListofScripData/w"
    )

    headers = {

        "User-Agent":
        "Mozilla/5.0",

        "Accept":
        "application/json"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print(
            "BSE download failed:",
            e
        )

        pd.DataFrame().to_csv(

            "database/companies/bse_companies.csv",

            index=False
        )

        return pd.DataFrame()

    companies = []

    for item in data:

        companies.append({

            "company_name":
            item.get(
                "Scrip_Name"
            ),

            "symbol":
            item.get(
                "Scrip_Code"
            ),

            "exchange":
            "BSE",

            "sector":
            "",

            "industry":
            "",

            "theme":
            "",

            "market_cap_type":
            "",

            "is_sme":
            False
        })

    bse = pd.DataFrame(
        companies
    )

    bse.to_csv(

        "database/companies/bse_companies.csv",

        index=False
    )

    print(
        "BSE:",
        len(bse)
    )

    return bse


# =====================================
# SME Companies
# =====================================

def download_sme():

    print(
        "\nDownloading SME companies..."
    )

    url = (
        "https://archives.nseindia.com/"
        "content/equities/"
        "EQUITY_L.csv"
    )

    df = pd.read_csv(
        url
    )

    if " SERIES" in df.columns:

        series_col = " SERIES"

    else:

        series_col = "SERIES"

    sme = df[
        df[
            series_col
        ]
        .astype(str)
        .str.contains(
            "SM",
            na=False
        )
    ]

    result = pd.DataFrame()

    result[
        "company_name"
    ] = sme[
        "NAME OF COMPANY"
    ]

    result[
        "symbol"
    ] = sme[
        "SYMBOL"
    ]

    result[
        "exchange"
    ] = "SME"

    result[
        "sector"
    ] = ""

    result[
        "industry"
    ] = ""

    result[
        "theme"
    ] = ""

    result[
        "market_cap_type"
    ] = "Micro"

    result[
        "is_sme"
    ] = True

    result.to_csv(

        "database/companies/sme_companies.csv",

        index=False
    )

    print(
        "SME:",
        len(result)
    )

    return result


# =====================================
# Master Dataset
# =====================================

def build_master():

    print(
        "\nBuilding master dataset..."
    )

    nse = pd.read_csv(
        "database/companies/nse_companies.csv"
    )

    bse = pd.read_csv(
        "database/companies/bse_companies.csv"
    )

    sme = pd.read_csv(
        "database/companies/sme_companies.csv"
    )

    final = pd.concat(

        [
            nse,
            bse,
            sme
        ],

        ignore_index=True
    )

    final = final.drop_duplicates(

        subset=[
            "company_name"
        ]
    )

    final.to_csv(

        "database/companies/all_companies.csv",

        index=False
    )

    print(
        "TOTAL:",
        len(final)
    )

    return final


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    download_nse()

    download_bse()

    download_sme()

    build_master()