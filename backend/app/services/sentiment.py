import re
from typing import Dict, Any, List

class FinSphereSentimentService:
    def __init__(self):
        # Local lexicon mapping financial terminologies to exact sentiment categories.
        # This provides robust CPU-speed fallback, fully compliant with offline guidelines.
        self.positive_keywords = {
            "robust", "growth", "improvement", "profitability", "synergy", "beat", "expansion",
            "outperform", "dividend", "guidance-up", "upside", "acceleration", "strong", "positive"
        }
        self.negative_keywords = {
            "headwinds", "decline", "deficit", "impairment", "contraction", "shortfall", "missed",
            "liquidity-concern", "downside", "decrease", "unfavorable", "lawsuit", "layoffs", "weak"
        }

    def analyze_paragraph_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Extracts financial sentiment from a text segment.
        Returns:
            Dict containing label (positive, negative, neutral) and score.
        """
        words = re.findall(r"\b\w+\b", text.lower())
        pos_count = sum(1 for w in words if w in self.positive_keywords)
        neg_count = sum(1 for w in words if w in self.negative_keywords)
        
        total_hits = pos_count + neg_count
        if total_hits == 0:
            return {"label": "neutral", "score": 0.50, "raw_score": 0.0}
            
        score = (pos_count - neg_count) / total_hits
        
        # Map score to label
        if score > 0.15:
            label = "positive"
            conf = 0.5 + (score * 0.5)
        elif score < -0.15:
            label = "negative"
            conf = 0.5 + (abs(score) * 0.5)
        else:
            label = "neutral"
            conf = 0.5
            
        return {
            "label": label,
            "score": float(conf),
            "raw_score": float(score)
        }

    def extract_key_statements(self, transcript_text: str) -> Dict[str, List[str]]:
        """
        Extracts guidance forecasts and risk statements from raw earnings transcript content.
        """
        lines = transcript_text.split("\n")
        guidance_patterns = [r"\bexpect\b", r"\bguidance\b", r"\bforecast\b", r"\boutlook\b", r"\btarget\b"]
        risk_patterns = [r"\brisks?\b", r"\bchallenges?\b", r"\buncertaint\w+\b", r"\bheadwinds?\b", r"\bthreats?\b"]
        
        guidance_extracts = []
        risk_extracts = []
        
        for line in lines:
            line_strip = line.strip()
            if len(line_strip) < 30:
                continue
                
            # Perform clean matches
            if any(re.search(pat, line_strip.lower()) for pat in guidance_patterns):
                if len(guidance_extracts) < 5:
                    guidance_extracts.append(line_strip)
            if any(re.search(pat, line_strip.lower()) for pat in risk_patterns):
                if len(risk_extracts) < 5:
                    risk_extracts.append(line_strip)
                    
        return {
            "guidance_statements": guidance_extracts,
            "risk_statements": risk_extracts
        }

sentiment_service = FinSphereSentimentService()
