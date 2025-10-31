from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
from typing import List, Dict, Any

app = FastAPI(title="Trace Collector")
TRACES: Dict[str, List[Dict[str, Any]]] = {}

@app.post("/ingest")
async def ingest_span(span: Dict[str, Any]):
    trace_id = span.get("trace_id")
    if not trace_id:
        return {"ok": False, "error": "missing trace_id"}
    if trace_id not in TRACES:
        TRACES[trace_id] = []
    span["received_at"] = datetime.utcnow().isoformat()
    TRACES[trace_id].append(span)
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = []
    for trace_id, spans in list(TRACES.items())[::-1]:
        rows.append(f"<h3>Trace {trace_id}</h3>")
        rows.append("<ul>")
        for s in spans:
            rows.append(f"<li><b>{s.get('service')}</b> → {s.get('operation')} ({s.get('duration_ms')} ms)</li>")
        rows.append("</ul>")
    html = f"""
    <html><head><title>TraceForge Collector</title>
    <style>body{{font-family:system-ui,sans-serif;padding:1.5rem;background:#0f172a;color:#e2e8f0}}
    h3{{color:#38bdf8}}ul{{background:#1e293b;padding:1rem;border-radius:.75rem}}</style></head>
    <body><h1>TraceForge Collector</h1>{''.join(rows) or '<p><em>No traces yet.</em></p>'}</body></html>
    """
    return HTMLResponse(content=html)
