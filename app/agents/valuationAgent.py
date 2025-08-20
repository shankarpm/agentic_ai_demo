import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.linear_model import LinearRegression

class ValuationAgent:
    def __init__(self, all_props: List[Dict[str, Any]]):
        df = pd.DataFrame(all_props)
        # Simple AVM features
        feats = ["sqft", "beds", "baths", "year_built"]
        df = df.dropna(subset=["price"])
        df[feats] = df[feats].fillna(df[feats].median())
        self.feats = feats
        self.avm = None
        if len(df) >= 40:
            X = df[feats].values
            y = df["price"].values
            self.avm = LinearRegression().fit(X, y)

    @staticmethod
    def compute_noi(rec: Dict[str, Any]) -> float:
        rent = float(rec.get("est_monthly_rent", 0.0))
        vacancy = float(rec.get("vacancy_rate", 0.07))
        taxes = float(rec.get("taxes", 0.0))
        insurance = float(rec.get("insurance", 0.0))
        maintenance = float(rec.get("maintenance", 0.0))
        hoa = float(rec.get("hoa", 0.0))
        gross = rent * 12.0 * (1.0 - vacancy)
        opex = taxes + insurance + maintenance + hoa
        return max(gross - opex, 0.0)

    @staticmethod
    def compute_cap_rate(noi: float, price: float) -> float:
        if price <= 0: return 0.0
        return noi / price

    @staticmethod
    def compute_coc_roi(noi: float, price: float, down_pct: float = 0.20) -> float:
        equity = price * down_pct
        if equity <= 0: return 0.0
        return noi / equity

    def compute_avm(self, rec: Dict[str, Any]) -> float:
        if self.avm is None:
            # fallback: price per sqft average of “nearby” (same city/state)
            sqft = rec.get("sqft", 1200) or 1200
            ppsf = 250.0
            return ppsf * sqft
        x = np.array([[rec.get("sqft", 1200), rec.get("beds", 3), rec.get("baths", 2.0), rec.get("year_built", 2005)]])
        return float(self.avm.predict(x)[0])

    def enrich(self, rec: Dict[str, Any]) -> Dict[str, Any]:
        price = float(rec["price"])
        noi = self.compute_noi(rec)
        cap = self.compute_cap_rate(noi, price)
        roi = self.compute_coc_roi(noi, price)
        avm = self.compute_avm(rec)
        out = dict(rec)
        out.update({
            "noi_annual": round(noi, 2),
            "cap_rate": round(cap, 4),
            "roi_cash_on_cash": round(roi, 4),
            "avm_price": round(avm, 2),
        })
        return out
