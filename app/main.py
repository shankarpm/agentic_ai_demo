import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from typing import List
from app.schemas import MatchRequest, MatchResponse, PropertyOut, ReportRequest, ReportResponse
from app.data_sources.csv_mls import CSVMLSAdapter
from app.orchestrator import AgenticOrchestrator

load_dotenv()

app = FastAPI(title="Agentic Real Estate Intelligence", version="0.1.0")

# Init data source + orchestrator
mls = CSVMLSAdapter.from_env_or_generate()
orc = AgenticOrchestrator(mls)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match", response_model=MatchResponse)
def match(req: MatchRequest):
    results = orc.match(
        location=req.location,
        property_types=req.property_types,
        price_min=req.price_min,
        price_max=req.price_max,
        min_bed=req.min_bed,
        min_bath=req.min_bath,
        min_cap_rate=req.min_cap_rate,
        n_results=req.n_results,
        preference_text=req.preference_text
    )
    out: List[PropertyOut] = []
    for r in results:
        out.append(PropertyOut(
            id=str(r["id"]),
            address=str(r["address"]),
            city=str(r["city"]),
            state=str(r["state"]),
            price=float(r["price"]),
            beds=int(r["beds"]),
            baths=float(r["baths"]),
            sqft=int(r["sqft"]),
            property_type=str(r["property_type"]),
            cap_rate=float(r["cap_rate"]),
            noi_annual=float(r["noi_annual"]),
            roi_cash_on_cash=float(r["roi_cash_on_cash"]),
            avm_price=float(r["avm_price"]),
            score=float(r["score"]),
        ))
    meta = {"count": len(out)}
    return MatchResponse(results=out, meta=meta)

@app.post("/report", response_model=ReportResponse)
def report(req: ReportRequest):
    props = []
    for pid in req.property_ids:
        try:
            p = mls.get_property(pid)
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Property not found: {pid}")
        # Ensure valuations present
        # (Orchestrator valuation requires list enrichment; do a quick enrich w/ single record)
        from app.agents.valuation_agent import ValuationAgent
        va = ValuationAgent(mls.list_properties())
        props.append(va.enrich(p))
    markdown = orc.report(req.investor_name, req.preferences_summary or "", props)
    return ReportResponse(markdown=markdown)
