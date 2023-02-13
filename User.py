from phe import paillier
import random

class User:

    bid = 0
    isBidAccepted = False
    payload = (0,0,0,0)

    def __init__(self, supplier):
        self.supplier = supplier

    def get_supplier(self):
        return self.supplier
    
    def get_bid(self):
        self.update_bid()
        return self.bid

    def set_accepted(self, accepted):
        self.isBidAccepted = accepted

    def get_payload(self):
        return self.payload

    def update_payload(self, payload_in):
        key = self.supplier.get_public_key()
        self.payload = (payload_in[0], payload_in[1], key.encrypt(payload_in[2]), key.encrypt(payload_in[3]), payload_in[4])