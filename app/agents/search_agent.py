from typing import List, Dict, Any, Optional

class SearchAgent:
    def __init__(self, mls_adapter):
        self.mls = mls_adapter

    def search(self,
               location: Optional[str],
               property_types: Optional[List[str]],
               price_min: Optional[float],
               price_max: Optional[float],
               min_bed: Optional[int],
               min_bath: Optional[float]) -> List[Dict[str, Any]]:
        records = self.mls.list_properties()
        def ok(r):
            if property_types and r["property_type"] not in property_types:
                return False
            if price_min and r["price"] < price_min:
                return False
            if price_max and r["price"] > price_max:
                return False
            if min_bed and r["beds"] < min_bed:
                return False
            if min_bath and r["baths"] < min_bath:
                return False
            if location:
                loc = f"{r['city']}, {r['state']}".lower()
                if location.lower() not in loc:
                    return False
            return True
        return [r for r in records if ok(r)]
