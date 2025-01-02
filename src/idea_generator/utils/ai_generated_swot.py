from typing import List, Tuple
from pydantic import BaseModel, Field


class WeightedSWOTFactor(BaseModel):
    """
    Represents a single SWOT factor with its description and weight.

    Attributes:
        description (str): A brief description of the factor.
        weight (float): Importance or impact weight (positive for opportunities/strengths, negative for threats/weaknesses).
    """
    description: str
    weight: float


class SWOTAnalysisQuantitative(BaseModel):
    """
    Represents a quantitative SWOT analysis with weighted factors.

    Attributes:
        strengths (List[WeightedSWOTFactor]): Weighted strengths.
        weaknesses (List[WeightedSWOTFactor]): Weighted weaknesses.
        opportunities (List[WeightedSWOTFactor]): Weighted opportunities.
        threats (List[WeightedSWOTFactor]): Weighted threats.
    """

    strengths: List[WeightedSWOTFactor] = Field(..., description="Weighted strengths")
    weaknesses: List[WeightedSWOTFactor] = Field(..., description="Weighted weaknesses")
    opportunities: List[WeightedSWOTFactor] = Field(..., description="Weighted opportunities")
    threats: List[WeightedSWOTFactor] = Field(..., description="Weighted threats")

    def calculate_net_positive_score(self) -> float:
        """
        Calculate the net positive score by summing the weights of strengths and opportunities,
        then subtracting the weights of weaknesses and threats.

        Returns:
            float: The net positive score.
        """
        positive_score = sum(factor.weight for factor in self.strengths + self.opportunities)
        negative_score = sum(factor.weight for factor in self.weaknesses + self.threats)
        return positive_score - negative_score

    def category_weight_summaries(self) -> dict:
        """
        Calculate total weights for each category (strengths, weaknesses, opportunities, threats).

        Returns:
            dict: Total weights for each SWOT category.
        """
        return {
            "strengths": sum(factor.weight for factor in self.strengths),
            "weaknesses": sum(factor.weight for factor in self.weaknesses),
            "opportunities": sum(factor.weight for factor in self.opportunities),
            "threats": sum(factor.weight for factor in self.threats),
        }

    def generate_swot_insights(self) -> List[str]:
        """
        Generate high-level insights based on SWOT analysis.

        Returns:
            List[str]: A list of insights derived from the SWOT analysis.
        """
        insights = []
        net_score = self.calculate_net_positive_score()
        category_summaries = self.category_weight_summaries()

        if net_score > 0:
            insights.append("The overall analysis indicates a positive outlook for the business idea.")
        elif net_score < 0:
            insights.append("The overall analysis indicates significant challenges that may outweigh benefits.")
        else:
            insights.append("The analysis is balanced; careful consideration of strengths and weaknesses is needed.")

        if category_summaries["opportunities"] > category_summaries["threats"]:
            insights.append("Opportunities outweigh threats, suggesting potential for growth.")
        else:
            insights.append("Threats outweigh opportunities; risk mitigation strategies are advised.")

        if category_summaries["strengths"] > category_summaries["weaknesses"]:
            insights.append("Strengths outweigh weaknesses, indicating a solid foundation.")
        else:
            insights.append("Weaknesses outweigh strengths; addressing these issues is critical.")

        return insights

    def rank_swot_impact(self) -> Tuple[List[str], List[str]]:
        """
        Rank factors by their impact within each category (highest to lowest).

        Returns:
            Tuple[List[str], List[str]]: Two lists containing the descriptions of the most and least impactful factors.
        """
        all_factors = self.strengths + self.weaknesses + self.opportunities + self.threats
        ranked_factors = sorted(all_factors, key=lambda factor: abs(factor.weight), reverse=True)

        most_impactful = [factor.description for factor in ranked_factors[:3]]
        least_impactful = [factor.description for factor in ranked_factors[-3:]]

        return most_impactful, least_impactful


# Example Usage
if __name__ == "__main__":
    swot_quant = SWOTAnalysisQuantitative(
        strengths=[
            WeightedSWOTFactor(description="Innovative technology", weight=8.0),
            WeightedSWOTFactor(description="Experienced team", weight=7.5),
        ],
        weaknesses=[
            WeightedSWOTFactor(description="High cost of implementation", weight=-6.0),
            WeightedSWOTFactor(description="Limited initial customer base", weight=-4.0),
        ],
        opportunities=[
            WeightedSWOTFactor(description="Growing market demand", weight=9.0),
            WeightedSWOTFactor(description="Partnership opportunities", weight=5.0),
        ],
        threats=[
            WeightedSWOTFactor(description="Strong competition", weight=-7.0),
            WeightedSWOTFactor(description="Economic downturn risks", weight=-5.5),
        ],
    )

    # Perform analysis
    print("Net Positive Score:", swot_quant.calculate_net_positive_score())
    print("Category Summaries:", swot_quant.category_weight_summaries())
    print("SWOT Insights:", swot_quant.generate_swot_insights())
    most, least = swot_quant.rank_swot_impact()
    print("Most Impactful Factors:", most)
    print("Least Impactful Factors:", least)
