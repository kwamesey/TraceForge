import os, time, httpx
from fastapi import FastAPI, Request

TRACE_COLLECTOR_URL = os.getenv("TRACE_COLLECTOR_URL", "http://localhost:8000")
RECS_URL = os.getenv("RECS_URL", "http://localhost:8003")
app = FastAPI(title="service-payments")

async def send_span(span: dict):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try: await client.post(f"{TRACE_COLLECTOR_URL}/ingest", json=span)
        except Exception: pass

@app.get("/pay")
async def pay(request: Request):
    trace_id = request.headers.get("X-TRACE-ID", f"no-trace-{int(time.time())}")
    start = time.time(); time.sleep(0.1)
    dur = int((time.time()-start)*1000)
    await send_span({"trace_id":trace_id,"service":"service-payments","operation":"charge-card","duration_ms":dur,"timestamp":int(time.time())})
    async with httpx.AsyncClient(timeout=5.0) as client:
        await client.get(f"{RECS_URL}/recs", headers={"X-TRACE-ID": trace_id})
    return {"ok":True,"trace_id":trace_id}
