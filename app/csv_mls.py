import os
import pandas as pd
from typing import List, Dict, Any
from .base import BaseMLSAdapter

class CSVMLSAdapter(BaseMLSAdapter):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    @classmethod
    def from_env_or_generate(cls):
        path = os.getenv("CSV_PATH")
        if path and os.path.exists(path):
            df = pd.read_csv(path)
        else:
            # Generate synthetic if no CSV
            from app.utils.data_gen import generate_synthetic_properties
            df = generate_synthetic_properties(n=500, city="Austin", state="TX")
        return cls(df)

    def list_properties(self) -> List[Dict[str, Any]]:
        return self.df.to_dict(orient="records")

    def get_property(self, pid: str) -> Dict[str, Any]:
        row = self.df[self.df["id"] == pid]
        if row.empty:
            raise KeyError(f"Property not found: {pid}")
        return row.iloc[0].to_dict()
