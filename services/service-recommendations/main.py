import os, time, httpx
from fastapi import FastAPI, Request

TRACE_COLLECTOR_URL = os.getenv("TRACE_COLLECTOR_URL", "http://localhost:8000")
app = FastAPI(title="service-recommendations")

async def send_span(span: dict):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try: await client.post(f"{TRACE_COLLECTOR_URL}/ingest", json=span)
        except Exception: pass

@app.get("/recs")
async def recs(request: Request):
    trace_id = request.headers.get("X-TRACE-ID", "no-trace")
    start = time.time(); time.sleep(0.03)
    dur = int((time.time()-start)*1000)
    await send_span({"trace_id":trace_id,"service":"service-recommendations","operation":"get-recs","duration_ms":dur,"timestamp":int(time.time())})
    return {"ok":True,"trace_id":trace_id,"recs":["item-1","item-2","item-3"]}
