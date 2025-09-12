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
class AdaptiveAgent:
    def __init__(self, agent_id, actions, state_space_size, target_price=50, min_price=40, max_price=60, quantity=10):
        self.agent_id = agent_id
        self.actions = actions
        self.state_space_size = state_space_size
        self.q_table = np.zeros((state_space_size, len(actions)))
        self.epsilon = 0.1
        self.alpha = 0.5
        self.gamma = 0.9

        # negotiation attributes
        self.target_price = float(target_price)
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.quantity = int(quantity)

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        return self.actions[np.argmax(self.q_table[state])]

    def update(self, state, action, reward, next_state):
        a_idx = self.actions.index(action)
        best_next = np.max(self.q_table[next_state])
        self.q_table[state, a_idx] += self.alpha * (reward + self.gamma * best_next - self.q_table[state, a_idx])

    def propose(self, last_offer_price=None):
        if last_offer_price is None:
            return self.target_price
        delta = last_offer_price - self.target_price
        return float(self.target_price + delta * 0.5)

    def utility(self, price: float) -> float:
        return 1.0 - abs(price - self.target_price) / max(1.0, abs(self.max_price - self.min_price))

    
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
    # Optionally, pass db_session if you want to record experiences in DB
    db_session = None
    try:
        from sqlmodel import Session, create_engine
        from .models import SQLModel
        import os
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
        engine = create_engine(DATABASE_URL, echo=False)
        db_session = Session(engine)
    except Exception:
        pass

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

        # --- AdaptiveAgent integration ---
        # If agents are AdaptiveAgent, record experience and update Q-table
        state = r - 1  # Example: use round number as state (customize as needed)
        next_state = r
        reward = fairness  # Example: use fairness as reward (customize as needed)
        if hasattr(buyer_agent, "update") and hasattr(buyer_agent, "record_experience"):
            buyer_agent.record_experience(db_session, state, bprice, reward, next_state)
            buyer_agent.update(state, bprice, reward, next_state)
        if hasattr(seller_agent, "update") and hasattr(seller_agent, "record_experience"):
            seller_agent.record_experience(db_session, state, sprice, reward, next_state)
            seller_agent.update(state, sprice, reward, next_state)

        # check acceptance: if seller offer close to buyer offer within threshold
        if abs(bprice - sprice) <= 1.0 or fairness >= 0.9:
            final_price = (bprice + sprice) / 2.0
            if db_session:
                db_session.close()
            return timeline, {"price": float(final_price), "quantity": buyer_agent.quantity, "fairness": fairness}
        last_buyer, last_seller = bprice, sprice
    # if max rounds reached, choose pareto best: pick midpoint of last offers
    lp = (last_buyer + last_seller) / 2.0
    if db_session:
        db_session.close()
    return timeline, {"price": float(lp), "quantity": buyer_agent.quantity, "fairness": timeline[-1]["fairness"] if timeline else 1.0}
