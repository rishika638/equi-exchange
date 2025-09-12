from eth_utils import keccak, to_bytes

def agreement_hash(buyer: str, seller: str, price: int, qty: int, delivery_days: int=0, escrow: bool=True) -> str:
    # canonical string -> hash
    s = f"{buyer.lower()}|{seller.lower()}|{price}|{qty}|{delivery_days}|{1 if escrow else 0}"
    h = keccak(text=s)
    return "0x" + h.hex()
