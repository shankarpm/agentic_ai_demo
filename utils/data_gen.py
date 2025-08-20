import numpy as np
import pandas as pd
from typing import Optional

def generate_synthetic_properties(n=500, city="Austin", state="TX", seed: Optional[int]=42) -> pd.DataFrame:
    if seed is not None:
        np.random.seed(seed)
    ids = [f"prop_{i:04d}" for i in range(n)]
    beds = np.random.choice([2,3,4,5], size=n, p=[0.2,0.45,0.3,0.05])
    baths = np.round(np.random.choice([1.0,1.5,2.0,2.5,3.0], size=n, p=[0.1,0.2,0.4,0.2,0.1]),1)
    sqft = np.random.normal(1800, 400, size=n).clip(800, 4000).astype(int)
    year = np.random.choice(range(1965,2022), size=n)
    price = (sqft * np.random.uniform(180, 350, size=n)) + (beds * 15000) + (baths * 10000)
    price = np.round(price / 1000, 0) * 1000
    rent = (sqft * np.random.uniform(0.8, 1.6, size=n)) + (beds * 50) + (baths * 40)
    hoa = np.random.choice([0, 50, 100, 200], size=n, p=[0.7,0.15,0.1,0.05])
    taxes = price * np.random.uniform(0.012, 0.022, size=n)
    insurance = np.random.uniform(800, 2500, size=n)
    maintenance = np.random.uniform(900, 2200, size=n)
    vacancy = np.random.uniform(0.04, 0.11, size=n)
    ptype = np.random.choice(["single_family","townhome","condo","duplex"], size=n, p=[0.6,0.2,0.15,0.05])
    desc = [f"{b}BR near tech hub, good schools, walkable area. Renovated {y}." for b,y in zip(beds,year)]
    lat = 30.2672 + np.random.uniform(-0.15,0.15,size=n)
    lon = -97.7431 + np.random.uniform(-0.15,0.15,size=n)

    df = pd.DataFrame({
        "id": ids,
        "address": [f"{np.random.randint(100,9999)} Main St" for _ in range(n)],
        "city": city, "state": state,
        "price": price,
        "beds": beds, "baths": baths, "sqft": sqft, "lot_sqft": sqft*3,
        "property_type": ptype,
        "hoa": hoa, "taxes": taxes, "insurance": insurance, "maintenance": maintenance,
        "vacancy_rate": vacancy, "est_monthly_rent": rent,
        "year_built": year, "description": desc,
        "lat": lat, "lon": lon
    })
    return df
