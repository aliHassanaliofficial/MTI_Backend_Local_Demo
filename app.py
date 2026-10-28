import sqlite3
from uuid import uuid4
from decimal import Decimal
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="MTI Local Engineering Demo", version="0.1.0")

def db():
    c = sqlite3.connect("mti_demo.sqlite3")
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,title TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS offers(id TEXT PRIMARY KEY,request_id TEXT NOT NULL REFERENCES requests(id),amount TEXT NOT NULL,currency TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS deals(id TEXT PRIMARY KEY,offer_id TEXT NOT NULL UNIQUE REFERENCES offers(id),status TEXT NOT NULL);
    """)
    return c

class RequestIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)

class OfferIn(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=20, decimal_places=4)
    currency: Literal["USD", "EGP", "EUR"]

@app.get("/health")
def health():
    return {"status":"ok","mode":"local_demo_only","real_money":False}

@app.post("/v1/trade-requests", status_code=201)
def create_request(body: RequestIn):
    id = str(uuid4())
    with db() as c:
        c.execute("INSERT INTO requests VALUES (?,?)", (id,body.title))
    return {"id":id,"title":body.title}

@app.get("/v1/trade-requests")
def list_requests():
    with db() as c:
        return [dict(r) for r in c.execute("SELECT * FROM requests")]

@app.post("/v1/trade-requests/{request_id}/offers", status_code=201)
def create_offer(request_id: str, body: OfferIn):
    with db() as c:
        if not c.execute("SELECT 1 FROM requests WHERE id=?",(request_id,)).fetchone():
            raise HTTPException(404,"Request not found")
        id = str(uuid4())
        c.execute("INSERT INTO offers VALUES (?,?,?,?)",(id,request_id,str(body.amount),body.currency))
    return {"id":id,"request_id":request_id,"amount":str(body.amount),"currency":body.currency}

@app.post("/v1/offers/{offer_id}/demo-deal", status_code=201)
def create_demo_deal(offer_id: str):
    with db() as c:
        if not c.execute("SELECT 1 FROM offers WHERE id=?",(offer_id,)).fetchone():
            raise HTTPException(404,"Offer not found")
        if c.execute("SELECT 1 FROM deals WHERE offer_id=?",(offer_id,)).fetchone():
            raise HTTPException(409,"Demo deal already exists")
        id = str(uuid4())
        c.execute("INSERT INTO deals VALUES (?,?,?)",(id,offer_id,"draft_demo"))
    return {"id":id,"offer_id":offer_id,"status":"draft_demo","binding_contract":False}

@app.get("/v1/deals/{deal_id}")
def get_deal(deal_id: str):
    with db() as c:
        row = c.execute("SELECT * FROM deals WHERE id=?",(deal_id,)).fetchone()
        if row is None:
            raise HTTPException(404,"Deal not found")
        return dict(row)
