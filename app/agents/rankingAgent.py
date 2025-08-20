import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RankingAgent:
    def __init__(self, min_cap_rate: Optional[float] = None, preference_text: Optional[str] = None):
        self.min_cap_rate = min_cap_rate or 0.0
        self.pref = preference_text or ""
        self.vectorizer = TfidfVectorizer(max_features=3000)

    def _preference_similarity(self, recs: List[Dict[str, Any]]) -> np.ndarray:
        corpus = [self.pref] + [r.get("description", "") for r in recs]
        X = self.vectorizer.fit_transform(corpus)
        sims = cosine_similarity(X[0:1], X[1:]).flatten()
        return sims

    @staticmethod
    def _normalize(arr: np.ndarray) -> np.ndarray:
        if len(arr) == 0: return arr
        mn, mx = np.min(arr), np.max(arr)
        if mx - mn < 1e-6:
            return np.ones_like(arr) * 0.5
        return (arr - mn) / (mx - mn)

    def rank(self, recs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not recs: return []
        cap = np.array([r.get("cap_rate", 0.0) for r in recs])
        roi = np.array([r.get("roi_cash_on_cash", 0.0) for r in recs])
        residual = np.array([abs(r.get("avm_price", r["price"]) - r["price"]) for r in recs])  # smaller is better
        pref_sim = self._preference_similarity(recs)

        cap_n = self._normalize(cap)
        roi_n = self._normalize(roi)
        residual_n = 1.0 - self._normalize(residual)  # invert

        # weights tuned for buy-and-hold; adjust per strategy
        score = 0.4 * cap_n + 0.3 * roi_n + 0.2 * residual_n + 0.1 * pref_sim
        for i, r in enumerate(recs):
            r["score"] = float(round(score[i], 4))

        # enforce min cap if provided
        if self.min_cap_rate:
            recs = [r for r in recs if r["cap_rate"] >= self.min_cap_rate]
        return sorted(recs, key=lambda x: x["score"], reverse=True)
