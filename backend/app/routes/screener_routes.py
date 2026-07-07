from typing import Optional

from fastapi import APIRouter

from app.agents.screener_agent import (
    ai_ranking,
    historical_ranking,
    get_cap_categories,
    get_sectors,
    get_industries
)

router = APIRouter()


# =====================================
# CAPS
# =====================================

@router.get("/caps")
def caps():

    return {
        "caps":
        get_cap_categories()
    }


# =====================================
# SECTORS
# =====================================

@router.get("/sectors")
def sectors(
        cap_category: str = "All"
):

    return {

        "sectors":

        get_sectors(
            cap_category
        )
    }


# =====================================
# INDUSTRIES
# =====================================

@router.get("/industries")
def industries(

        cap_category: str = "All",

        sector: str = "All"
):

    return {

        "industries":

        get_industries(

            cap_category,

            sector
        )
    }


# =====================================
# AI RANKING
# =====================================

@router.get("/ranking/ai")
def ai(

        cap_category: str = "All",

        sector: str = "All",

        industry: str = "All",

        top_n: Optional[int] = None
):

    return ai_ranking(

        cap_category,

        sector,

        industry,

        top_n
    ).to_dict(
        orient="records"
    )


# =====================================
# HISTORICAL RANKING
# =====================================

@router.get("/ranking/historical")
def historical(

        cap_category: str = "All",

        sector: str = "All",

        industry: str = "All",

        period: str = "1y",

        top_n: Optional[int] = None
):

    return historical_ranking(

        cap_category,

        sector,

        industry,

        period,

        top_n
    ).to_dict(
        orient="records"
    )
