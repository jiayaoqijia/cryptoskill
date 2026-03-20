"""
pump.fun Token Sniper Scorer - Paid API
Scores new tokens 0-100 for snipe safety. Pay-per-request via x402.
"""

import os, sys, json
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from scorer import score_token

app = FastAPI(title="pump.fun Sniper Scorer API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

PRICE = os.environ.get("PRICE_PER_REQUEST", "0.05")
PAY_TO = os.environ.get("PAY_TO_ADDRESS", "")
FACILITATOR = os.environ.get("FACILITATOR_URL", "https://x402.org/facilitator")
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


def payment_requirements():
    return {
        "x402Version": 1,
        "accepts": [{
            "scheme": "exact", "network": "base",
            "maxAmountRequired": str(int(float(PRICE) * 1_000_000)),
            "resource": "/score", "description": f"pump.fun token snipe score — ${PRICE} per request",
            "mimeType": "application/json", "payTo": PAY_TO,
            "maxTimeoutSeconds": 60, "asset": USDC_BASE,
        }],
        "error": "Payment required"
    }


def verify_payment(request: Request) -> bool:
    if not PAY_TO:
        return True
    ph = request.headers.get("X-PAYMENT")
    if not ph:
        return False
    try:
        r = requests.post(f"{FACILITATOR}/verify",
                          json={"payment": ph, "paymentRequirements": payment_requirements()["accepts"][0]},
                          timeout=10)
        return r.status_code == 200 and r.json().get("isValid", False)
    except Exception:
        return False


def settle_payment(ph: str) -> dict:
    try:
        r = requests.post(f"{FACILITATOR}/settle",
                          json={"payment": ph, "paymentRequirements": payment_requirements()["accepts"][0]},
                          timeout=10)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}


@app.get("/")
def root():
    idx = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(idx):
        return FileResponse(idx)
    return {"name": "pump.fun Sniper Scorer API", "price": f"${PRICE} USDC/request",
            "endpoint": "GET /score?ca=<TOKEN_CA>"}


@app.get("/health")
def health():
    return {"status": "ok", "payment_configured": bool(PAY_TO)}


@app.get("/demo")
async def demo(ca: str):
    """Free endpoint for web UI users"""
    if not ca or len(ca) < 32:
        raise HTTPException(400, "Invalid CA")
    try:
        r = score_token(ca)
        return {
            "ca": r.ca,
            "score": r.total_score,
            "verdict": r.verdict,
            "token": r.token_meta,
            "breakdown": r.breakdown,
            "signals": r.signals,
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/score")
async def score(ca: str, request: Request):
    """
    Score a pump.fun token for snipe safety (0-100).
    Requires x402 payment of ${PRICE} USDC per request.

    Parameters:
        ca: Token contract address (mint)

    Returns:
        score (0-100), verdict (SNIPE/CAUTION/AVOID), breakdown, signals
    """
    if not ca or len(ca) < 32:
        raise HTTPException(400, "Invalid CA")

    if PAY_TO:
        ph = request.headers.get("X-PAYMENT")
        if not ph:
            return Response(content=json.dumps(payment_requirements()),
                            status_code=402, headers={"Content-Type": "application/json"})
        if not verify_payment(request):
            raise HTTPException(402, "Invalid or expired payment")

    try:
        r = score_token(ca)
        result = {
            "ca": r.ca,
            "score": r.total_score,
            "verdict": r.verdict,
            "token": r.token_meta,
            "breakdown": r.breakdown,
            "signals": r.signals,
        }
        if PAY_TO:
            ph = request.headers.get("X-PAYMENT")
            if ph:
                settlement = settle_payment(ph)
                return Response(content=json.dumps(result), status_code=200,
                                headers={"Content-Type": "application/json",
                                         "X-PAYMENT-RESPONSE": json.dumps(settlement)})
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
