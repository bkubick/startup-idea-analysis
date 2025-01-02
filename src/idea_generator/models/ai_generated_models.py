from pydantic import BaseModel, Field
from typing import List, Optional
import math


from typing import List, Optional
from pydantic import BaseModel, Field


class BusinessIdea(BaseModel):
    """
    Represents a detailed business idea with contextual, financial, and operational information.

    Attributes:
        name (str): The name of the business idea.
        description (str): A high-level description of the business concept.
        details (str): Detailed information about the business model, operations, and objectives.
        industry (str): The industry category the business belongs to.
        sub_industry (Optional[str]): More specific sub-category of the industry.
        target_market (str): Description of the target market or audience.
        unique_value_proposition (str): The unique selling point that differentiates this business from competitors.
        market_cap (float): Estimated market capitalization (in USD).
        competitors (List[str]): List of key competitors in the industry.
        growth_rate (float): Estimated annual growth rate of the industry (percentage).
        initial_investment (float): Estimated required initial investment (in USD).
        potential_revenue (float): Estimated annual revenue potential (in USD).
        profit_margin (float): Expected profit margin (percentage).
        target_audience_size (int): Size of the potential target audience.
        customer_acquisition_cost (float): Average cost to acquire a new customer (in USD).
        customer_lifetime_value (float): Average lifetime value of a customer (in USD).
        market_saturation (float): Percentage of target market already served (percentage).
        business_stage (str): The current stage of the business (e.g., "Idea", "Prototype", "Early Revenue", "Scaling").
        funding_sources (List[str]): Potential or current funding sources (e.g., "Bootstrapped", "Venture Capital").
        team_size (Optional[int]): Number of team members currently working on the business.
        key_resources (List[str]): Key resources or assets the business relies on (e.g., patents, partnerships).
        potential_risks (List[str]): Potential risks or challenges facing the business idea.
    """
    name: str = Field(..., description="The name of the business idea")
    description: str = Field(..., description="A high-level description of the business concept")
    details: str = Field(..., description="Detailed information about the business model, operations, and objectives")
    industry: str = Field(..., description="The industry category the business belongs to")
    sub_industry: Optional[str] = Field(None, description="More specific sub-category of the industry")
    target_market: str = Field(..., description="Description of the target market or audience")
    unique_value_proposition: str = Field(..., description="The unique selling point that differentiates this business")
    market_cap: float = Field(..., description="Estimated market capitalization (in USD)")
    competitors: List[str] = Field(..., description="List of key competitors in the industry")
    growth_rate: float = Field(..., description="Estimated annual growth rate of the industry (percentage)")
    initial_investment: float = Field(..., description="Estimated required initial investment (in USD)")
    potential_revenue: float = Field(..., description="Estimated annual revenue potential (in USD)")
    profit_margin: float = Field(..., description="Expected profit margin (percentage)")
    target_audience_size: int = Field(..., description="Size of the potential target audience")
    customer_acquisition_cost: float = Field(..., description="Average cost to acquire a new customer (in USD)")
    customer_lifetime_value: float = Field(..., description="Average lifetime value of a customer (in USD)")
    market_saturation: float = Field(..., description="Percentage of target market already served (percentage)")
    business_stage: str = Field(..., description="The current stage of the business")
    funding_sources: List[str] = Field(..., description="Potential or current funding sources")
    team_size: Optional[int] = Field(None, description="Number of team members currently working on the business")
    key_resources: List[str] = Field(..., description="Key resources or assets the business relies on")
    potential_risks: List[str] = Field(..., description="Potential risks or challenges facing the business idea")


class SWOTAnalysis(BaseModel):
    """
    Represents a SWOT analysis.

    Attributes:
        strengths (List[str]): Key strengths of the business idea.
        weaknesses (List[str]): Key weaknesses of the business idea.
        opportunities (List[str]): Opportunities for growth or market entry.
        threats (List[str]): Threats to the business idea.
    """
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class BusinessAnalysisResult(BaseModel):
    """
    Represents the result of analyzing a business idea.

    Attributes:
        business_name (str): Name of the business idea.
        industry (str): Industry category of the business.
        roi_percentage (float): Calculated ROI as a percentage.
        market_attractiveness (float): Score representing market attractiveness.
        competitor_density (float): Score representing the density of competitors.
        payback_period_years (float): Estimated time in years to recover the initial investment.
        customer_profitability (float): Net profitability of acquiring a customer (LTV - CAC).
        market_saturation_score (float): Score representing market saturation (lower is better).
        rank_score (float): Overall rank score of the business idea.
        swot_analysis (Optional[SWOTAnalysis]): Qualitative SWOT analysis data.
    """
    business_name: str
    industry: str
    roi_percentage: float
    market_attractiveness: float
    competitor_density: float
    payback_period_years: float
    customer_profitability: float
    market_saturation_score: float
    rank_score: float
    swot_analysis: Optional[SWOTAnalysis] = None


def calculate_roi(potential_revenue: float, profit_margin: float, initial_investment: float) -> float:
    """
    Calculate the Return on Investment (ROI).

    Args:
        potential_revenue (float): Estimated annual revenue potential (in USD).
        profit_margin (float): Expected profit margin (as a percentage).
        initial_investment (float): Estimated required initial investment (in USD).

    Returns:
        float: ROI as a percentage.
    """
    profit = (potential_revenue * (profit_margin / 100))
    roi = (profit - initial_investment) / initial_investment * 100
    return roi


def calculate_competitor_density(market_cap: float, competitors: List[str]) -> float:
    """
    Calculate the competitor density within the market.

    Args:
        market_cap (float): Estimated market capitalization (in USD).
        competitors (List[str]): List of major competitors.

    Returns:
        float: Competitor density (market cap per competitor).
    """
    return market_cap / len(competitors) if competitors else 0


def calculate_market_attractiveness(growth_rate: float, competitor_density: float) -> float:
    """
    Assess market attractiveness based on growth rate and competitor density.

    Args:
        growth_rate (float): Estimated annual growth rate of the industry (as a percentage).
        competitor_density (float): Score representing the density of competitors.

    Returns:
        float: Market attractiveness score.
    """
    return growth_rate / competitor_density if competitor_density > 0 else 0


def calculate_payback_period(initial_investment: float, annual_profit: float) -> float:
    """
    Calculate the payback period to recover the initial investment.

    Args:
        initial_investment (float): Estimated required initial investment (in USD).
        annual_profit (float): Annual profit (in USD).

    Returns:
        float: Payback period in years (infinity if annual profit is zero or negative).
    """
    return initial_investment / annual_profit if annual_profit > 0 else math.inf


def calculate_market_saturation_score(market_saturation: float) -> float:
    """
    Evaluate market saturation, where lower saturation is better.

    Args:
        market_saturation (float): Percentage of target market already served (as a percentage).

    Returns:
        float: Market saturation score (normalized to range 0-1).
    """
    return max(0, 100 - market_saturation) / 100


def calculate_customer_profitability(lifetime_value: float, acquisition_cost: float) -> float:
    """
    Calculate the profitability of acquiring a customer.

    Args:
        lifetime_value (float): Average lifetime value of a customer (in USD).
        acquisition_cost (float): Average cost to acquire a new customer (in USD).

    Returns:
        float: Customer profitability (LTV - CAC).
    """
    return lifetime_value - acquisition_cost


def rank_business_idea(business: BusinessIdea, swot: Optional[SWOTAnalysis] = None) -> BusinessAnalysisResult:
    """
    Rank the business idea based on several metrics.

    Args:
        business (BusinessIdea): The business idea to evaluate.
        swot (Optional[SWOTAnalysis]): Optional SWOT analysis for qualitative evaluation.

    Returns:
        BusinessAnalysisResult: A summary of the analysis and ranking score.
    """
    roi = calculate_roi(
        business.potential_revenue, business.profit_margin, business.initial_investment)
    competitor_density = calculate_competitor_density(
        business.market_cap, business.competitors)
    market_attractiveness = calculate_market_attractiveness(
        business.growth_rate, competitor_density)
    payback_period = calculate_payback_period(
        business.initial_investment, business.potential_revenue * (business.profit_margin / 100))
    customer_profitability = calculate_customer_profitability(
        business.customer_lifetime_value, business.customer_acquisition_cost)
    market_saturation_score = calculate_market_saturation_score(
        business.market_saturation)

    # Simple weighting of scores to calculate overall rank
    rank_score = (
        roi * 0.3 +
        market_attractiveness * 0.2 +
        market_saturation_score * 0.2 +
        customer_profitability * 0.2 -
        payback_period * 0.1
    )

    return BusinessAnalysisResult(
        business_name=business.name,
        industry=business.industry,
        roi_percentage=roi,
        market_attractiveness=market_attractiveness,
        competitor_density=competitor_density,
        payback_period_years=payback_period,
        customer_profitability=customer_profitability,
        market_saturation_score=market_saturation_score,
        rank_score=rank_score,
        swot_analysis=swot
    )
