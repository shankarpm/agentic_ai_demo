# Agentic Real Estate Intelligence (Agentic-REI)

A production-ready skeleton for an Agentic AI system that:
- Matches residential/commercial properties to investor preferences
- Computes CAP rate, NOI, cash-on-cash ROI, and a simple AVM
- Ranks candidates and generates an investor-ready summary report
- Exposes clean APIs for integration with CRMs, dashboards, or n8n/Zapier

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env   # set OPENAI_API_KEY if you want LLM-generated reports
uvicorn app.main:app --reload
