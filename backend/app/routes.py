from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, create_engine
from .models import Session as SessionModel, Offer, Agreement, SQLModel
from .agents import BaseAgent, run_negotiation_loop
from .utils import agreement_hash
import os
from typing import Dict

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)

@router.post("/sessions")
def create_session(payload: Dict):
    # expected fields: role ('buyer' or 'seller'), buyer_address, seller_address, target/min/max price, quantity, fairness_weight, max_rounds
    with Session(engine) as db:
        s = SessionModel(
            role=payload.get("role","buyer"),
            buyer_address=payload.get("buyer_address"),
            seller_address=payload.get("seller_address"),
            target_price=payload.get("target_price"),
            min_price=payload.get("min_price"),
            max_price=payload.get("max_price"),
            quantity=payload.get("quantity"),
            fairness_weight=payload.get("fairness_weight", 0.5),
            max_rounds=payload.get("max_rounds", 8),
            status="open"
        )
        db.add(s)
        db.commit()
        db.refresh(s)
        return {"session_id": s.id, "session": s}

@router.post("/sessions/{session_id}/auto")
def run_auto(session_id: int):
    with Session(engine) as db:
        s = db.get(SessionModel, session_id)
        if not s:
            raise HTTPException(status_code=404, detail="session not found")
        # create buyer and seller agents using addresses and provided targets
        # For demo, if buyer_address missing, use a synthetic one
        buyer_addr = s.buyer_address or "0x000000000000000000000000000000000000b0y"
        seller_addr = s.seller_address or "0x0000000000000000000000000000000000005e11"
        buyer_agent = BaseAgent(buyer_addr, s.target_price or s.max_price or 90, s.min_price or 50, s.max_price or 100, s.quantity or 1, s.fairness_weight)
        seller_agent = BaseAgent(seller_addr, s.max_price or 100, s.min_price or 50, s.max_price or 120, s.quantity or 1, s.fairness_weight)
        timeline, agreement = run_negotiation_loop(buyer_agent, seller_agent, max_rounds=s.max_rounds or 8)
        # persist offers as Offer rows
        round_idx = 1
        for r in timeline:
            o = Offer(
                session_id=session_id,
                round=r["round"],
                made_by="buyer",
                price=r["buyer_offer"],
                quantity=agreement["quantity"],
                fairness=r["fairness"],
                utility=r["buyer_util"],
                payload=str(r)
            )
            db.add(o)
            o2 = Offer(
                session_id=session_id,
                round=r["round"],
                made_by="seller",
                price=r["seller_offer"],
                quantity=agreement["quantity"],
                fairness=r["fairness"],
                utility=r["seller_util"],
                payload=str(r)
            )
            db.add(o2)
            round_idx += 1
        # persist Agreement
        ag_hash = agreement_hash(buyer_addr, seller_addr, int(round(agreement["price"])), int(agreement["quantity"]))
        ag = Agreement(session_id=session_id, price=agreement["price"], quantity=agreement["quantity"], agreement_hash=ag_hash)
        db.add(ag)
        s.status = "finalized"
        db.commit()
        db.refresh(ag)
        return {"timeline": timeline, "agreement": {"price": agreement["price"], "quantity": agreement["quantity"], "fairness": agreement["fairness"], "agreement_hash": ag_hash}}

@router.get("/sessions/{session_id}/timeline")
def get_timeline(session_id: int):
    with Session(engine) as db:
        q = db.exec(select(Offer).where(Offer.session_id == session_id).order_by(Offer.round))
        offers = q.all()
        return {"offers": [o.dict() for o in offers]}

@router.post("/sessions/{session_id}/finalize")
def finalize(session_id: int):
    with Session(engine) as db:
        ag_q = db.exec(select(Agreement).where(Agreement.session_id == session_id))
        ag = ag_q.first()
        if not ag:
            raise HTTPException(status_code=404, detail="agreement not found")
        # return canonical agreement info so frontend can call the contract
        # We also return buyer/seller addresses stored in session for signing
        sess = db.get(SessionModel, session_id)
        return {
            "agreement_hash": ag.agreement_hash,
            "price": ag.price,
            "quantity": ag.quantity,
            "buyer_address": sess.buyer_address,
            "seller_address": sess.seller_address
        }
