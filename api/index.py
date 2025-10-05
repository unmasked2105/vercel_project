from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/api/metrics")
async def metrics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    # Load your telemetry bundle here (simulate or read from file/db)
    # Example structure: {"region": "emea", "latency": 150, "uptime": 0.99}
    import json
    with open("telemetry.json") as f:
        data = json.load(f)

    results = {}
    for region in regions:
        region_data = [d for d in data if d["region"] == region]
        latencies = [d["latency"] for d in region_data]
        uptimes = [d["uptime"] for d in region_data]

        if not region_data:
            continue

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = sum(1 for l in latencies if l > threshold)

        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    return results
