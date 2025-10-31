import os, time, uuid, httpx
from fastapi import FastAPI

TRACE_COLLECTOR_URL = os.getenv("TRACE_COLLECTOR_URL", "http://localhost:8000")
PAYMENTS_URL = os.getenv("PAYMENTS_URL", "http://localhost:8002")
app = FastAPI(title="service-auth")

async def send_span(span: dict):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try: await client.post(f"{TRACE_COLLECTOR_URL}/ingest", json=span)
        except Exception: pass

@app.get("/auth")
async def auth_flow():
    trace_id = str(uuid.uuid4())
    start = time.time(); time.sleep(0.05)
    dur = int((time.time()-start)*1000)
    await send_span({"trace_id":trace_id,"service":"service-auth","operation":"login","duration_ms":dur,"timestamp":int(time.time())})
    async with httpx.AsyncClient(timeout=5.0) as client:
        await client.get(f"{PAYMENTS_URL}/pay", headers={"X-TRACE-ID": trace_id})
    return {"ok":True,"trace_id":trace_id}
