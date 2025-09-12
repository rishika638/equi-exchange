import numpy as np
from typing import Tuple, Dict

class WhaleManager:
    def __init__(self, threshold_share=0.2):
        self.threshold_share = threshold_share
    def detect(self, holdings_share: float) -> bool:
        return holdings_share >= self.threshold_share

class WashTradeDetector:
    def __init__(self):
        pass
    def suspicious(self, recent_pairs: list) -> bool:
        # naive: if same addresses trade repeatedly in small window -> suspicious
        if len(recent_pairs) < 4:
            return False
        return len(set(recent_pairs[-4:])) < 4

class FeeOptimizer:
    def __init__(self):
        pass
    def estimate_fee(self, gas_price_gwei: float, gas_used: int=21000):
        return gas_price_gwei * 1e-9 * gas_used

class Reputation:
    def __init__(self):
        self.scores = {}  # address -> score
    def get(self, addr):
        return self.scores.get(addr, 0.5)
    def update(self, addr, delta):
        self.scores[addr] = max(0.0, min(1.0, self.get(addr) + delta))

class Limits:
    def __init__(self, max_offers=20):
        self.max_offers = max_offers
    def allowed(self, offer_count):
        return offer_count < self.max_offers

# Negotiation Agents
class BaseAgent:
    def __init__(self, address: str, target_price: float, min_price: float, max_price: float, quantity: int, fairness_weight=0.5):
        self.address = address
        self.target_price = float(target_price)
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.quantity = int(quantity)
        self.fairness_weight = fairness_weight
        self.concession_rate = 0.05  # default concession per round

    def propose(self, last_offer_price: float=None) -> float:
        # simple heuristic: if no last offer, propose target; else move half-way toward last offer
        if last_offer_price is None:
            return self.target_price
        # concede fractionally
        delta = last_offer_price - self.target_price
        return float(self.target_price + delta * 0.5)

    def utility(self, price: float) -> float:
        # higher price better for seller, lower better for buyer — normalized 0..1
        # assume this agent is buyer if target price < max_price? (we'll set role outside)
        # utility is simple distance from target
        return 1.0 - abs(price - self.target_price) / max(1.0, abs(self.max_price - self.min_price))

# A simple orchestrator
def run_negotiation_loop(buyer_agent: BaseAgent, seller_agent: BaseAgent, max_rounds=8):
    timeline = []
    last_buyer = None
    last_seller = None
    for r in range(1, max_rounds+1):
        # buyer proposes
        bprice = buyer_agent.propose(last_seller)
        buyer_util = buyer_agent.utility(bprice)
        # seller responds
        sprice = seller_agent.propose(bprice)
        seller_util = seller_agent.utility(sprice)
        # fairness score
        fairness = 1.0 - abs(buyer_util - seller_util)
        timeline.append({
            "round": r,
            "buyer_offer": float(bprice),
            "seller_offer": float(sprice),
            "buyer_util": float(buyer_util),
            "seller_util": float(seller_util),
            "fairness": float(fairness)
        })
        # check acceptance: if seller offer close to buyer offer within threshold
        if abs(bprice - sprice) <= 1.0 or fairness >= 0.9:
            final_price = (bprice + sprice) / 2.0
            return timeline, {"price": float(final_price), "quantity": buyer_agent.quantity, "fairness": fairness}
        last_buyer, last_seller = bprice, sprice
    # if max rounds reached, choose pareto best: pick midpoint of last offers
    lp = (last_buyer + last_seller) / 2.0
    return timeline, {"price": float(lp), "quantity": buyer_agent.quantity, "fairness": timeline[-1]["fairness"] if timeline else 1.0}
