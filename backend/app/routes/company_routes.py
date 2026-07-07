from fastapi import APIRouter

from app.agents.screener_agent import get_company_details
from app.agents.report_agent import generate_report
from app.agents.news_agent import get_news
from app.agents.historical_agent import get_price_history   # NEW

router = APIRouter()


@router.get("/company/{company_name}")
def company(company_name):
    return get_company_details(company_name)


@router.get("/company/{company_name}/news")
def company_news(company_name):
    return get_news({"company_name": company_name})


# =====================================
# COMPANY PRICE HISTORY (NEW)
# =====================================

@router.get("/company/{company_name}/history")
def company_history(company_name, period: str = "1y"):

    details = get_company_details(company_name)

    if details is None:
        return []

    return get_price_history(
        {"symbol": details["symbol"]},
        period
    )


@router.get("/company/{company_name}/report")
def company_report(company_name):
    company = get_company_details(company_name)
    if company is None:
        return {}
    return company