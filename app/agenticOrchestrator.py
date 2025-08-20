from typing import List, Dict, Any, Optional
from app.agents.search_agent import SearchAgent
from app.agents.valuation_agent import ValuationAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.report_agent import ReportAgent

class AgenticOrchestrator:
    def __init__(self, mls_adapter):
        self.search_agent = SearchAgent(mls_adapter)
        self._all_props = mls_adapter.list_properties()
        self.valuation_agent = ValuationAgent(self._all_props)
        self.report_agent = ReportAgent()

    def match(self,
              location: Optional[str],
              property_types: Optional[List[str]],
              price_min: Optional[float],
              price_max: Optional[float],
              min_bed: Optional[int],
              min_bath: Optional[float],
              min_cap_rate: Optional[float],
              n_results: int,
              preference_text: Optional[str]) -> List[Dict[str, Any]]:
        base = self.search_agent.search(location, property_types, price_min, price_max, min_bed, min_bath)
        enriched = [self.valuation_agent.enrich(r) for r in base]
        ranker = RankingAgent(min_cap_rate=min_cap_rate, preference_text=preference_text)
        ranked = ranker.rank(enriched)
        return ranked[:max(1, n_results)]

    def report(self, investor_name: str, preferences_summary: str, props: List[Dict[str, Any]]) -> str:
        return self.report_agent.generate(investor_name, preferences_summary, props)
