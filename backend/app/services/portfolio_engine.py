from typing import Dict, Any, List

class FinSpherePortfolioEngine:
    def __init__(self):
        # Default target asset classes
        self.asset_classes = {
            "fixed_income": "Bonds / US Treasuries",
            "index_funds": "S&P 500 Index ETF",
            "blue_chip": "Stable Large-Cap Corporate Equities",
            "growth_equities": "High-Beta Tech & Sector Growth Stocks",
            "emerging_assets": "Small-Cap & Strategic Volatility Hedging"
        }

    def generate_recommendations(self, risk_profile: str, target_sectors: List[str] = None, 
                                 investment_objectives: str = "") -> Dict[str, Any]:
        """
        Calculates optimized allocations based on user input profile.
        """
        profile = risk_profile.lower()
        sectors = target_sectors or ["Technology", "Healthcare", "Financials"]
        
        # Determine allocations (weights sum to 100)
        if profile == "conservative":
            allocations = [
                {"asset": self.asset_classes["fixed_income"], "weight": 55, "color": "#6366F1"}, # Slate Indigo
                {"asset": self.asset_classes["index_funds"], "weight": 25, "color": "#10B981"}, # Emerald
                {"asset": self.asset_classes["blue_chip"], "weight": 15, "color": "#FBBF24"}, # Amber
                {"asset": self.asset_classes["growth_equities"], "weight": 5, "color": "#EF4444"}, # Crimson
                {"asset": self.asset_classes["emerging_assets"], "weight": 0, "color": "#EC4899"}
            ]
            explanation = (
                "Your profile defaults to conservative risk tolerance. We allocate 55% to Fixed Income "
                "Bonds & US Treasuries to guarantee capital preservation. S&P Index ETF index tracking builds "
                "stable matching equity trends, while growth exposure is capped to prevent drawdown periods."
            )
        elif profile == "balanced":
            allocations = [
                {"asset": self.asset_classes["fixed_income"], "weight": 30, "color": "#6366F1"},
                {"asset": self.asset_classes["index_funds"], "weight": 35, "color": "#10B981"},
                {"asset": self.asset_classes["blue_chip"], "weight": 20, "color": "#FBBF24"},
                {"asset": self.asset_classes["growth_equities"], "weight": 10, "color": "#EF4444"},
                {"asset": self.asset_classes["emerging_assets"], "weight": 5, "color": "#EC4899"}
            ]
            explanation = (
                "A balanced approach splits capital across growth indexes and security buffers. "
                "We designate 35% to index tracking S&P ETF, backed by 30% in high-grade bonds, "
                "supporting moderate growth with limited exposure to unexpected market volatility."
            )
        else: # aggressive
            allocations = [
                {"asset": self.asset_classes["fixed_income"], "weight": 10, "color": "#6366F1"},
                {"asset": self.asset_classes["index_funds"], "weight": 20, "color": "#10B981"},
                {"asset": self.asset_classes["blue_chip"], "weight": 25, "color": "#FBBF24"},
                {"asset": self.asset_classes["growth_equities"], "weight": 35, "color": "#EF4444"},
                {"asset": self.asset_classes["emerging_assets"], "weight": 10, "color": "#EC4899"}
            ]
            explanation = (
                "Aggressive allocations maximize alpha. 35% is weighted towards technology growth assets, "
                "supported by 10% in high-yield emerging plays. Fixed income capital shields are lowered to 10%, "
                "exposing capital to high market trends with structural target metrics."
            )
            
        # Target sectors weighting summary
        sector_allocation = {}
        total_sectors = len(sectors)
        if total_sectors > 0:
            weight_per_sector = round(100.0 / total_sectors, 1)
            for s in sectors:
                sector_allocation[s] = weight_per_sector
                
        return {
            "risk_profile": risk_profile.capitalize(),
            "allocations": [a for a in allocations if a["weight"] > 0],
            "sector_weightings": sector_allocation,
            "explanation": explanation,
            "financial_advisory_clause": "Model output based on quantitative risk indexes. Direct asset consultation advised prior to major trades."
        }

portfolio_engine = FinSpherePortfolioEngine()
